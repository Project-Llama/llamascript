import subprocess
import os
import sys

i = input("Are you sure you don't want to create a gh release instead? (Y/n): ")

if i == "n":
    sys.exit(0)
elif i == "Y":
    if os.path.exists("dist"):
        subprocess.run(["rm", "-r", "dist"])
    if os.path.exists("build"):
        subprocess.run(["rm", "-r", "build"])
    if os.path.exists("llamascript.egg-info"):
        subprocess.run(["rm", "-r", "llamascript.egg-info"])
    
    subprocess.run(["python3", "setup.py", "sdist", "bdist_wheel"])
    subprocess.run(["twine", "upload", "dist/*"])
sys.exit(0)
