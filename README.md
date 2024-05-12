<div style="border-radius: 20px;" align="center">
  <img width="128" height="128" src="https://github.com/Project-Llama/.github/blob/main/profile/IMG_1443.png">
</div>

# LlamaScript

[Medium Post](https://medium.com/@wolfthedev/llamascript-simple-ai-builder-74442dc9b090)

[![Black Format](https://github.com/Project-Llama/llamascript/actions/workflows/format.yml/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/format.yml)
[![Upload to PyPi](https://github.com/Project-Llama/llamascript/actions/workflows/python-publish.yml/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/python-publish.yml)
[![CodeQL](https://github.com/Project-Llama/llamascript/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/WolfTheDeveloper/llamascript/actions/workflows/github-code-scanning/codeql)

[![VS Code Extension Downloads](https://img.shields.io/visual-studio-marketplace/d/WolfTheDev.llamascript?label=VS-Code%20Downloads)](https://marketplace.visualstudio.com/items?itemName=WolfTheDev.llamascript)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Project-Llama/llamascript?label=Commits)
![GitHub License](https://img.shields.io/github/license/Project-Llama/llamascript?label=License)

LlamaScript is a no-code AI chatbot using Ollama.

## Table of Contents
- [LlamaScript](#llamascript)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
  - [Roadmap](#roadmap)
  - [Examples](examples/)

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

> [!NOTE]\
> For more examples see [here.](examples/)

You can then run LlamaScript with the following command:

```bash
llamascript
```

LlamaScript usually has a file extension of `.llama`, but if it is ran as a main script, it is usually `llama` (no file extension).

## License
LlamaScript is licensed under the Apache 2.0 License.

## Roadmap
Things to come in the future:

- An `API` command to serve on Flask
- Plugins/Extensions handling (Help Wanted)

