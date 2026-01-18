# cnb_cli/utils/helper.py
from pathlib import Path
from loguru import logger

def create_file(file_path: str, content: str):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        logger.info(f"File '{file_path}' already exists. No changes were made.")
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"File '{file_path}' has been created successfully.")

def modify_file(file_path: str, content: str):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if content.strip() in existing:
            logger.info(f"Content already exists in file '{file_path}'. No changes were made.")
            return

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"File '{file_path}' has been modified successfully.")
