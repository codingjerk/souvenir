from pathlib import Path
import os


def create_directory(directory: Path) -> None:
    os.makedirs(directory)


def create_file(file: Path) -> None:
    with open(file, "w"):
        pass
