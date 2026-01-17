# cnb_cli/utils/fs.py

from pathlib import Path

def mkdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def touch(path: str):
    Path(path).touch(exist_ok=True)

def write_file(path: str, content: str):
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    if not file.exists():
        file.write_text(content)
