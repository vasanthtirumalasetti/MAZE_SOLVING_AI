import subprocess

python_files = ["main.py", "pdf.py"]

for file in python_files:
    subprocess.run(["python", file])
