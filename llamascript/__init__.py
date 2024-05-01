import asyncio
import ollama
import logging

# Set up logging
logging.basicConfig(level=logging.WARNING)


class llama:
    def __init__(self):
        self.model = ""
        self.data = ""
        self.system = []
        self.ignore = False

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
                response = ollama.chat(
                    model=self.model,
                    messages=self.system + [{"role": "user", "content": self.data}],
                    stream=stream,
                )
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

    async def read(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    command = line.split(" ")
                    if command[0] == "IGNORE":
                        self.ignore = True
                    elif command[0] == "USE":
                        self.USE(line)
                    elif len(command) > 1 and command[1] == "INPUT":
                        self.INPUT(command[0])
                    elif command[0] == "SYSTEM":
                        self.SYSTEM(line=line)
                    elif command[0] == "PROMPT":
                        self.PROMPT(line=line)
                    elif command[0] == "CHAT" and command[1] == "STREAM":
                        stream = command[1] == True if len(command) > 1 else False
                        if not self.ignore:
                            print(
                                '=================\nThanks for using llama, a no-code AI chatbot. Please ensure Ollama (https://ollama.com) is running. To get started, type "USE" followed by the model you want to use. Then, type "PROMPT" followed by the prompt you want to use. Finally, type "CHAT" to chat with the AI. To run a script, type "llamascript" to run your script. To ignore this message, add "IGNORE" to the beginning of your llama file.\n================='
                            )
                            self.ignore = True
                        self.CHAT(stream=stream)
                    else:
                        raise ValueError("Invalid command")
        except FileNotFoundError:
            logging.error("File %s not found.", filename)
            print(f"File {filename} not found.")


def run():
    try:
        l = llama()
        asyncio.run(l.read("llama"))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
