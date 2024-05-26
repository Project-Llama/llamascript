import subprocess
import os

if os.path.exists("dist"):
    subprocess.run(["rm", "-r", "dist"])
if os.path.exists("build"):
    subprocess.run(["rm", "-r", "build"])
if os.path.exists("llamascript.egg-info"):
    subprocess.run(["rm", "-r", "llamascript.egg-info"])

subprocess.run(["python3", "setup.py", "sdist", "bdist_wheel"])
subprocess.run(["twine", "upload", "dist/*"])
