import random
import sys
import termios
import tty
from pathlib import Path
from typing import Dict

import yaml
from tabulate import tabulate


class Deck:
    def __init__(self, cards) -> None:
        self.cards = cards

    @staticmethod
    def load(path: Path) -> "Deck":
        with open(path, "r") as file:
            cards = yaml.safe_load(file.read())

        return Deck(cards)


class BucketStats:
    def __init__(self, path: Path, buckets: Dict[int, int], key: str) -> None:
        self.path = path
        self.buckets = buckets
        self.key = key

    @staticmethod
    def load(path: Path, key: str) -> "BucketStats":
        try:
            with open(path, "r") as file:
                buckets = yaml.safe_load(file.read())
        except FileNotFoundError:
            buckets = {}

        return BucketStats(path, buckets, key)

    def card_id(self, card) -> int:
        if self.key not in card:
            return hash(str(card))

        return hash(self.key) + hash(card[self.key])

    def bucket_of(self, card) -> int:
        card_id = self.card_id(card)
        bucket = self.buckets.get(card_id, 1)
        assert 1 <= bucket

        return bucket

    def select_cards(self, cards, count: int) -> "LearningSample":
        sample = []
        while len(sample) < count:
            for card in cards:
                select_prob = 1 / self.bucket_of(card) / len(cards)

                if random.random() < select_prob:
                    sample.append(card)

                if len(sample) >= count:
                    break

        return LearningSample(sample, self.key)

    def update(self, learning_sample: "LearningSample") -> None:
        for card in learning_sample.hits:
            self.move_card(card, +1)

        for card in learning_sample.misses:
            self.move_card(card, -1)

    def move_card(self, card, delta: int) -> None:
        card_id = self.card_id(card)
        bucket = self.bucket_of(card)

        self.buckets[card_id] = max(bucket + delta, 1)

    def save(self) -> None:
        with open(self.path, "w") as file:
            yaml.safe_dump(self.buckets, file)


class LearningSample:
    def __init__(self, cards, key: str) -> None:
        self.cards = cards
        self.key = key

        self.hits = []
        self.misses = []

    def run_interactive(self):
        for card in self.cards:
            if not self.key in card:
                continue

            self.show_question(card)
            correct = self.ask_if_correct(card)

            if correct:
                self.hits.append(card)
            else:
                self.misses.append(card)

        self.show_results()

    def show_results(self) -> None:
        print("=> session results")

        hits = self.cards_to_key_string(self.hits)
        misses = self.cards_to_key_string(self.misses)
        print(f"  * hits:   {len(self.hits)} ({hits})")
        print(f"  * misses: {len(self.misses)} ({misses})")

    def cards_to_key_string(self, cards) -> str:
        return ", ".join(
            card[self.key]
            for card in cards
            if self.key in card
        )

    def show_question(self, card) -> None:
        question = card[self.key]

        print(f"=> {question}", end=" ", flush=True)
        self.getch()
        print()

    def ask_if_correct(self, card) -> bool:
        correct = None
        while correct not in {"n", "y"}:
            self.show_answer(card)
            print("=| correct? [y/n]", end=" ", flush=True)
            correct = self.getch()
            print()
        print()

        return correct == "y"

    def show_answer(self, card) -> None:
        for key, value in card.items():
            if key == self.key:
                continue

            print(f"   {key}: {value}")

    @staticmethod
    def getch() -> str:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        if ord(ch) == 3:
            exit(1)

        return ch


def sv_list(deck_name: str) -> None:
    deck = Deck.load(Path(deck_name + ".yml"))

    print(tabulate(
        deck.cards,
        headers="keys",
        tablefmt="psql",
    ))


def sv_repeat(deck_name: str, key: str, card_count: int) -> None:
    deck = Deck.load(Path(deck_name + ".yml"))
    bucket_stats = BucketStats.load(Path(deck_name + ".bts.yml"), key)

    learning_sample = bucket_stats.select_cards(deck.cards, card_count)
    learning_sample.run_interactive()

    bucket_stats.update(learning_sample)
    bucket_stats.save()
