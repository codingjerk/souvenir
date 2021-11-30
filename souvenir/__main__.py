from pathlib import Path

import typer

from souvenir.fsutils import create_directory, create_file
from souvenir.gitutils import git_add, git_commit, git_init
from souvenir.svutils import sv_add, sv_list, sv_repeat

sv = typer.Typer()


@sv.command()
def new(deck_name: str) -> None:
    deck_directory = Path(deck_name)

    create_directory(deck_directory)
    create_file(deck_directory.joinpath("deck.csv"))

    git_init(deck_directory)
    git_add("deck.csv")
    git_commit("Initial commit")


@sv.command()
def add(question: str, answer: str) -> None:
    sv_add(question, answer)


@sv.command()
def list() -> None:
    sv_list()


@sv.command()
def repeat(times: int = 10) -> None:
    sv_repeat(times)


if __name__ == "__main__":
    sv()
