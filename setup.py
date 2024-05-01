import setuptools

setuptools.setup(
    name="llamascript",
    version="0.2.0",
    author="WolfTheDev",
    author_email="wolfthedev@gmail.com",
    description="No-code AI chatbot using Ollama.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/WolfTheDeveloper/llamascript",
    packages=setuptools.find_packages(),
    install_requires=["ollama"],
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
