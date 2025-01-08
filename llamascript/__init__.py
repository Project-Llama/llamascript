__version__ = "1.0.1"

import ollama
import logging
import sys
import subprocess
import os
import platform
import re
import argparse
import colorama

colorama.init()
dbg = False


def debug(message):
    if dbg:
        print(
            f"{colorama.Fore.CYAN}{colorama.Style.BRIGHT}[DEBUG]{colorama.Style.RESET_ALL} {message}"
        )


def error(message):
    print(
        f"{colorama.Fore.RED}{colorama.Style.BRIGHT}[ERROR]{colorama.Style.RESET_ALL} {message}"
    )


def warning(message):
    print(
        f"{colorama.Fore.YELLOW}{colorama.Style.BRIGHT}[WARNING]{colorama.Style.RESET_ALL} {message}"
    )


def info(message):
    print(
        f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}[INFO]{colorama.Style.RESET_ALL} {message}"
    )


# Set up logging
logging.basicConfig(level=logging.WARNING)


class Lexer:
    def __init__(self, input_text):
        self.tokens = []
        self.tokenize(input_text)

    def tokenize(self, text):
        token_specification = [
            ("ATTRIBUTE", r"#\[(.*?)\]"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("STRING", r"\".*?\""),
            ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("COMMA", r","),
            ("NEWLINE", r"\n"),
            ("SKIP", r"[ \t]+"),
            ("SLC", r"//.*"),
            ("MLC", r"/\*(.|\n)*?\*/"),
            ("MISMATCH", r"."),
        ]
        tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "NUMBER":
                value = float(value) if "." in value else int(value)
                self.tokens.append(("NUMBER", value))
            elif kind in {"ID", "STRING", "LPAREN", "RPAREN", "COMMA", "ATTRIBUTE"}:
                self.tokens.append((kind, value))
            elif kind == "NEWLINE":
                self.tokens.append(("NEWLINE", value))
            elif kind == "SKIP":
                continue
            elif kind == ("SLC" or "MLC"):
                continue
            elif kind == "MISMATCH":
                error(f"Invalid character: {value}")
                sys.exit(1)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        ast = []
        current_attributes = {}
        while self.current < len(self.tokens):
            token = self.tokens[self.current]
            if token[0] == "ATTRIBUTE":
                current_attributes = self.parse_attribute(
                    token[1][2:-1].strip()
                )  # Remove #[ and ]
                self.current += 1  # Skip ATTRIBUTE
            elif token[0] == "ID":
                ast.append(self.statement(current_attributes))
                current_attributes = {}  # Reset after associating
            else:
                self.current += 1
        return ast

    def statement(self, attributes):
        token = self.tokens[self.current]
        func_name = token[1].lower()
        self.current += 1  # Skip function name

        if self.tokens[self.current][0] != "LPAREN":
            error(f"Expected '(' after {func_name}")
            sys.exit(1)

        self.current += 1  # Skip '('
        args = self.arguments()

        if self.tokens[self.current][0] != "RPAREN":
            error("Expected ')' after arguments")
            sys.exit(1)

        self.current += 1  # Skip ')'
        return (func_name, args, attributes)

    def arguments(self):
        args = []
        while (
            self.current < len(self.tokens) and self.tokens[self.current][0] != "RPAREN"
        ):
            token = self.tokens[self.current]
            if token[0] == "STRING":
                args.append(token[1][1:-1])  # Strip surrounding quotes
                self.current += 1
            elif token[0] == "NUMBER":
                args.append(token[1])
                self.current += 1
            elif token[0] == "COMMA":
                self.current += 1  # Skip comma
            else:
                error(f"Invalid argument `{token[1]}`")
                sys.exit(1)
        return args

    def parse_attribute(self, attr_str):
        match = re.match(r"(\w+)\((.+)\)", attr_str)
        if match:
            attr_name = match.group(1).lower()
            attr_value = match.group(2).strip('"').strip("'")
            if attr_value.lower() == "true":
                attr_value = True
            elif attr_value.lower() == "false":
                attr_value = False
            return {attr_name: attr_value}
        else:
            error(f"Invalid attribute: {attr_str}")
            sys.exit(1)


class Interpreter:
    def __init__(self, ast, llama_instance):
        self.ast = ast
        self.llama = llama_instance

    def execute(self):
        for node in self.ast:
            command = node[0]
            args = node[1]
            attributes = node[2]
            if command == "use":
                self.llama.use(args[0], attributes)
            elif command == "prompt":
                self.llama.prompt(args[0], attributes)
            elif command == "system":
                self.llama.system_command(args[0], attributes)
            elif command == "save":
                self.llama.create_model(
                    args[0],
                    {
                        "model": self.llama.model,
                        "temperature": args[1],
                        "system_message": self.llama.system[0]["content"],
                    },
                    attributes,
                )
            elif command == "chat":
                self.llama.chat(attributes)
            else:
                raise ValueError(f"Unknown command: {command}")


class Llama:
    def __init__(self):
        self.model = ""
        self.data = ""
        self.system = []

    def use(self, model_name, _):
        self.model = model_name.strip('"')
        debug(f"Using model: {self.model}")

    def prompt(self, prompt_text, attributes):
        if "input" in attributes:
            self.data = input(prompt_text)
        else:
            self.data = prompt_text
        debug(f"Prompt set to: {self.data}")

    def system_command(self, system_content, _):
        self.system = [{"role": "system", "content": system_content}]
        debug(f"System command set.")

    def chat(self, attributes):
        stream = attributes.get("stream", False)
        debug(f"Stream set to: {stream}")
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
                    warning(
                        "Streaming is a work in progress. Please wait for the final response."
                    )
                    for message in response:
                        print(message["message"]["content"], end="")
                    print()
                else:
                    print(response["message"]["content"])
                break
            except Exception as e:
                logging.error("Error using model: %s", e)
                debug("Model not loaded. Trying to load model...")
                ollama.pull(self.model)
                debug("Model loaded. Trying again...")
        else:
            error("Error using model. Please try again.")
            sys.exit(1)

    def create_model(self, filename, parameters, attributes):
        try:
            with open(filename, "w") as file:
                file.write(
                    f'FROM {parameters["model"]}\nPARAMETER temperature {parameters["temperature"]}\nSYSTEM """\n{parameters["system_message"]}\n"""\n'
                )
            debug("Modelfile created.")
            command = ["ollama", "create", parameters["model"], "-f", "./Modelfile"]
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
            info("Model created.")

            if process.returncode != 0:
                if stderr:
                    error(f"Error executing command: {stderr.decode()}")
                elif stdout:
                    debug(stdout.decode())
            debug("Removing Modelfile...")
            os.remove(filename)

        except Exception as e:
            logging.error("Error creating model file: %s", e)
            error(f"Error creating model file {filename}.")
            sys.exit(1)

    def read(self, filename):
        try:
            with open(filename, "r") as file:
                content = file.read()
                lexer = Lexer(content)
                parser = Parser(lexer.tokens)
                ast = parser.parse()
                interpreter = Interpreter(ast, self)
                interpreter.execute()
        except FileNotFoundError:
            logging.error("File %s not found.", filename)
            error(f"File {filename} not found.")


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
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug mode",
    )

    args = parser.parse_args()

    global dbg
    dbg = args.debug

    if not args.file_name.endswith(".llama"):
        err_msg = "Invalid file type. Please provide a .llama."
        logging.error(err_msg)
        error(err_msg)
        sys.exit(1)

    try:
        l = Llama()
        l.read(args.file_name)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
