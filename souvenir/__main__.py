from pathlib import Path

import typer

from souvenir.utils import create_directory, create_file
from souvenir.git import git_add, git_commit, git_init

sv = typer.Typer()


@sv.command()
def new(deck_name: str) -> None:
    deck_directory = Path(deck_name)

    create_directory(deck_directory)
    create_file(deck_directory.joinpath("deck.csv"))
    git_init(deck_directory)
    git_add("deck.csv")
    git_commit(deck_directory, "Initial commit")


@sv.command()
def add(question: str, answer: str) -> None:
    pass


@sv.command()
def list() -> None:
    pass


@sv.command()
def repeat() -> None:
    pass


if __name__ == "__main__":
    sv()
