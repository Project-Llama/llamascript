# LlamaScript

[![Black Format](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/format.yml/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/format.yml)
[![Upload to PyPi](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/python-publish.yml/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/python-publish.yml)
[![CodeQL](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/github-code-scanning/codeql)
[![Test](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/test.yml/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/test.yml)

LlamaScript is a no-code AI chatbot using Ollama.

## Installation

You can install LlamaScript using pip:

```bash
pip install llamascript
```

## Usage
To use LlamaScript, create a llama file (no file extension) with the following commands:

```llamascript
IGNORE: Use this before the CHAT command to supress the welcome message.
USE <model>: This command loads the specified model.
SYSTEM <message>: This command sets the system prompt.
PROMPT <message>: This command sets the message to be sent to the chatbot.
CHAT: This command sends the message to the chatbot and prints the response.
```

Here's an example:

```llamascript
IGNORE
USE llama3
PROMPT Hello, how are you?
CHAT
```

You can then run LlamaScript with the following command:

```bash
llamascript
```

## License
LlamaScript is licensed under the Apache 2.0 License.
