import typer

from souvenir.svutils import sv_list, sv_repeat

sv = typer.Typer()


@sv.command()
def list(deck: str) -> None:
    sv_list(deck)


@sv.command()
def repeat(deck: str, key: str, times: int = 10) -> None:
    sv_repeat(deck, key, times)


if __name__ == "__main__":
    sv()
