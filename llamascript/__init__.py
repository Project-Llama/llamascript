__version__ = "0.6.5"

import asyncio
import ollama
import logging
import sys
import subprocess
import os
import platform

dbg = False


def debug(message):
    if dbg:
        print(message)


# Set up logging
logging.basicConfig(level=logging.WARNING)


class llama:
    def __init__(self):
        self.model = ""
        self.data = ""
        self.system = []

    def USE(self, line):
        if line.split(" ")[0] == "USE":
            self.model = line.split(" ")[1].strip()
        else:
            raise ValueError("Invalid model")

    def PROMPT(self, line="", p=""):
        if p != "":
            self.data = p
        else:
            split_line = line.split(" ", 1)
            self.data = split_line[1] if len(split_line) > 1 else ""

    def SYSTEM(self, line="", p=""):
        if p != "":
            self.system = [{"role": "system", "content": p}]
        else:
            split_line = line.split(" ", 1)
            prompt = split_line[1] if len(split_line) > 1 else ""
            self.system = [{"role": "system", "content": prompt}]

    def CHAT(self, stream: bool = False):
        for _ in range(3):
            try:
                debug("Attempting to chat with model...")
                response = ollama.chat(
                    model=self.model,
                    messages=self.system + [{"role": "user", "content": self.data}],
                    stream=stream,
                )
                debug("Chat successful.")
                if stream:
                    for message in response:
                        print(message["message"]["content"], end="")
                    print()
                else:
                    print(response["message"]["content"])
                break
            except Exception as e:
                logging.error("Error using model: %s", e)
                print("Model not loaded. Trying to load model...")
                ollama.pull(self.model)
                print("Model loaded. Trying again...")
        else:
            raise ValueError(
                "Model does not exist or could not be loaded. Please try again."
            )

    def INPUT(self, command):
        if command == "SYSTEM":
            self.SYSTEM(p=input("Enter system prompt: "))
        elif command == "PROMPT":
            self.PROMPT(p=input("Enter prompt: "))
        else:
            raise ValueError("Invalid command for INPUT")

    def CREATE_MODEL(self, filename, parameters, model_name):
        try:
            with open(filename, "w") as file:
                file.write(
                    f'FROM {parameters["model"]}\nPARAMETER temperature {parameters["temperature"]}\nSYSTEM """\n{parameters["system_message"]}\n"""\n'
                )
            print(f"Modelfile created.")
            command = ["ollama", "create", model_name, "-f", "./Modelfile"]
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            else:
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            stdout, stderr = process.communicate()
            print("Model created.")

            if process.returncode != 0:
                if stderr is not None:
                    print(f"Error executing command: {stderr.decode()}")
                else:
                    if stdout is not None:
                        print(stdout.decode())
            print("Removing Modelfile...")
            os.remove(filename)

        except Exception as e:
            logging.error("Error creating model file: %s", e)
            print(f"Error creating model file {filename}.")
            sys.exit(1)

    def execute_command(self, command):
        if command.startswith("PROMPT INPUT"):
            self.INPUT("PROMPT")
        elif command.startswith("CHAT"):
            self.CHAT()
        else:
            raise ValueError("Invalid command to repeat")

    async def read(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                i = 0
                while i < len(lines):
                    line = lines[i].strip()
                    if not line:
                        i += 1
                        continue
                    command = line.split(" ")
                    if command[0] == "USE":
                        self.USE(line)
                    elif len(command) > 1 and command[1] == "INPUT":
                        self.INPUT(command[0])
                    elif command[0] == "SYSTEM":
                        self.SYSTEM(line=line)
                    elif command[0] == "PROMPT":
                        self.PROMPT(line=line)
                    elif command[0] == "SAVE":
                        if len(command) < 2:
                            logging.error("No filename provided")
                            print("No filename provided")
                            sys.exit(1)
                        model_name = command[1]
                        parameters = {
                            "model": self.model,
                            "temperature": command[2] if len(command) > 2 else 0.7,
                            "system_message": self.system[0]["content"],
                        }
                        self.CREATE_MODEL("Modelfile", parameters, model_name)
                    elif command[0] == "CHAT":
                        if len(command) > 1 and command[1] == "STREAM":
                            self.CHAT(stream=True)
                        else:
                            self.CHAT()
                    else:
                        raise ValueError("Invalid command")
                    i += 1
        except FileNotFoundError:
            logging.error("File %s not found.", filename)
            print(f"File {filename} not found.")


import argparse


def run():
    parser = argparse.ArgumentParser(description="Run llama script.")
    parser.add_argument("file_name", type=str, help="The name of the file to run")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"LlamaScript version {__version__}",
        help="Display version information",
    )

    args = parser.parse_args()

    if not (args.file_name.endswith(".llama") or args.file_name == "llama"):
        logging.error("Invalid file type. Please provide a .llama or llama file.")
        print("Invalid file type. Please provide a .llama or llama file.")
        sys.exit(1)

    try:
        l = llama()
        asyncio.run(l.read(args.file_name))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
