<div style="border-radius: 20px;" align="center">
  <img width="128" height="128" src="https://github.com/Project-Llama/.github/blob/main/profile/IMG_1443.png">
</div>

# LlamaScript
[![Black Format](https://github.com/Project-Llama/llamascript/actions/workflows/format.yml/badge.svg)](https://github.com/Project-Llama/llamascript/actions/workflows/format.yml)
[![Upload to PyPi](https://github.com/Project-Llama/llamascript/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Project-Llama/llamascript/actions/workflows/python-publish.yml)
[![CodeQL](https://github.com/Project-Llama/llamascript/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/Project-Llama/llamascript/actions/workflows/github-code-scanning/codeql)

[![VS Code Extension Downloads](https://img.shields.io/visual-studio-marketplace/d/zanderlewis.llamascript?label=VS-Code%20Downloads)](https://marketplace.visualstudio.com/items?itemName=zanderlewis.llamascript)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Project-Llama/llamascript?label=Commits)
![GitHub License](https://img.shields.io/github/license/Project-Llama/llamascript?label=License)

LlamaScript is a no-code AI chatbot using Ollama.

## Table of Contents
- [LlamaScript](#llamascript)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)
- [Examples](https://github.com/Project-Llama/llamascript/blob/main/examples/)

## Installation

You can install LlamaScript using pip:

```bash
pip install llamascript
```

## Usage
To use LlamaScript, create a `.llama` file and write your script. Here are a few functions you can use:
```llamascript
use(...)    // Specify the model to use
prompt(...) // Prompt the user for input
system(...) // System message for the AI
chat(...)   // Chat with the user
save(...)   // Save the model
```

Here's an example:
```llamascript
use("llama3")
prompt("Why is the sky blue?")
chat()
```

> [!NOTE]\
> For more examples see [here.](https://github.com/Project-Llama/llamascript/blob/main/examples/)

You can then run LlamaScript with the following command:
```bash
llamascript myscript.llama
```

## License
LlamaScript is licensed under the Apache 2.0 License. See [LICENSE](https://github.com/Project-Llama/llamascript/blob/main/LICENSE) for more information.
