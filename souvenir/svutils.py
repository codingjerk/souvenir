import random
import sys
import termios
import tty
from dataclasses import dataclass
from typing import List

from tabulate import tabulate

from souvenir.gitutils import git_add, git_commit


class Card:
    def __init__(
        self,
        question: str,
        answer: str,
        views: int = 0,
        hits: int = 0,
        misses: int = 0,
    ):
        self.question = str(question)
        self.answer = str(answer)
        self.views = int(views)
        self.hits = int(hits)
        self.misses = int(misses)

    def to_csv(self) -> str:
        return "\t".join(self.to_row()) + "\n"

    def to_row(self) -> List[str]:
        return [
            self.question,
            self.answer,
            str(self.views),
            str(self.hits),
            str(self.misses),
        ]


Deck = List[Card]


def sv_add(question: str, answer: str) -> None:
    with open("deck.csv", "a") as deck_fh:
        card = Card(question, answer)
        deck_fh.write(card.to_csv())

    git_add("deck.csv")
    git_commit(f'auto: add question "{question}"')


def sv_list() -> None:
    deck = sv_deck()
    print(tabulate(
        [card.to_row() for card in deck],
        headers=["Question", "Answer", "Views", "Hits", "Misses"],
        tablefmt="psql",
    ))


def sv_repeat(times: int) -> None:
    deck = sv_deck()
    sample = select_hardest_cards(deck, times)

    hits = []
    misses = []
    for card in sample:
        print(f" [ ? ] => {card.question}", end=" ", flush=True)
        getch()
        print()

        answer = None
        while answer not in {"n", "y"}:
            print(f" [y/n] => {card.answer}", end=" ", flush=True)
            answer = getch()
            print()
        print()

        card.views += 1

        if answer == "y":
            card.hits += 1
            hits.append(card.question)
        else:
            card.misses += 1
            misses.append(card.question)

    print("Session stats:")
    print(f"  * Hits:   {len(hits)} ({', '.join(set(hits))})")
    print(f"  * Misses: {len(misses)} ({', '.join(set(misses))})")

    sv_save(deck)


def select_hardest_cards(deck: Deck, count: int) -> Deck:
    sample = []
    while len(sample) < count:
        for card in deck:
            select_prob = 1 * (card.misses or 1) / (len(deck) or 1) / (card.views or 1)
            if random.random() < select_prob:
                sample.append(card)

            if len(sample) >= count:
                break

    return sample


def sv_save(deck: Deck) -> None:
    with open("deck.csv", "w") as deck_fh:
        for card in deck:
            deck_fh.write(card.to_csv())


def sv_deck() -> Deck:
    deck = []

    with open("deck.csv", "r") as deck_fh:
        for line in deck_fh.readlines():
            args = line.strip().split("\t")
            card = Card(*args)
            deck.append(card)

    return deck


def getch() -> str:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch
