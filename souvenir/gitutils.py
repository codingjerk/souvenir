import os
from pathlib import Path

from git import Repo


def git_add(file: str) -> None:
    Repo().index.add([file])


def git_commit(message: str) -> None:
    Repo().index.commit(message)


def git_init(directory: Path) -> None:
    Repo.init(directory, mkdir=True)
    os.chdir(directory)
