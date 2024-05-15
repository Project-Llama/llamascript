import subprocess

subprocess.run(["python3", "setup.py", "sdist", "bdist_wheel"])
subprocess.run(["twine", "upload", "dist/*"])