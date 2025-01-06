import setuptools
import os
import re


def read_version():
    with open(os.path.join("llamascript", "__init__.py")) as f:
        return re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)


setuptools.setup(
    name="llamascript",
    version=read_version(),
    author="Zander Lewis",
    author_email="zander@zanderlewis.dev",
    description="No-code AI chatbot using Ollama.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Project-Llama/llamascript",
    packages=setuptools.find_packages(),
    install_requires=["ollama", "colorama"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "llamascript=llamascript:run",
        ],
    },
)
