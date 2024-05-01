import asyncio
import ollama
import logging
import unittest

# Set up logging
logging.basicConfig(level=logging.INFO)


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

    def PROMPT(self, line):
        if line.split(" ", 1)[0] == "PROMPT":
            self.data = line.split(" ", 1)[1]
        else:
            raise ValueError("Invalid data")

    def SYSTEM(self, line):
        if line.split(" ", 1)[0] == "SYSTEM":
            prompt = line.split(" ", 1)[1]
            self.system = [{"role": "system", "content": prompt}]
        else:
            raise ValueError("Invalid system prompt.")

    def CHAT(self):
        for _ in range(3):  # Try 3 times
            try:
                print(
                    ollama.chat(
                        model=self.model,
                        messages=self.system + [{"role": "user", "content": self.data}],
                    )["message"]["content"]
                )
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

    async def read(self, filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    command = line.split(" ")[0]
                    if command == "IGNORE":
                        self.ignore = True
                    elif command == "USE":
                        self.USE(line)
                    elif command == "SYSTEM":
                        self.SYSTEM(line)
                    elif command == "PROMPT":
                        self.PROMPT(line)
                    elif command == "CHAT":
                        if not self.ignore:
                            print(
                                '=================\nThanks for using llama, a no-code AI chatbot. Please ensure Ollama (https://ollama.com) is running. To get started, type "USE" followed by the model you want to use. Then, type "PROMPT" followed by the prompt you want to use. Finally, type "CHAT" to chat with the AI. To run a script, type "llamascript" to run your script. To ignore this message, add "IGNORE" to the beginning of your llama file.\n================='
                            )
                            self.ignore = True
                        self.CHAT()
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
