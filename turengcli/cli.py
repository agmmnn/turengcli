from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from urllib.parse import quote

from curl_cffi import requests
from rich import box
from rich import print as rprint
from rich.console import Console
from rich.table import Table

API_URL = "https://api.tureng.com/v3/Dictionary/entr/{term}"
AUTOCOMPLETE_URL = "https://ac.tureng.co/?t={term}"
TURENG_URL = "https://tureng.com/en/turkish-english/{term}"
API_HEADERS = {
    "Accept": "application/json",
    "Tureng-Client-Id": "tureng-android",
    "Tureng-Api-Key": "b7e2c4d9f1a0635c8e2d7b4a9f6c1e3d5a8b0c2f4d6e7a9b1c3d5f7e8a0b2c4",
    "Tureng-Client-Version": "4.3.36",
}


@dataclass(frozen=True)
class Direction:
    exact_key: str
    full_text_key: str
    source_field: str
    target_field: str
    source_label: str
    target_label: str


EN_TO_TR = Direction("aResults", "aFullTextResults", "termA", "termB", "EN", "TR")
TR_TO_EN = Direction("bResults", "bFullTextResults", "termB", "termA", "TR", "EN")


class TurengDict:
    def __init__(self, word, args):
        self.word = word.strip()
        self.args = args

        if self.args.fuzzy:
            self.fuzzy()
            return

        self.payload = self.lookup(self.word)
        self.main()

    @staticmethod
    def lookup(word: str) -> dict:
        response = requests.get(
            API_URL.format(term=quote(word, safe="")),
            headers=API_HEADERS,
            impersonate="chrome",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def autocomplete(word: str) -> list[str]:
        response = requests.get(
            AUTOCOMPLETE_URL.format(term=quote(word, safe="")),
            impersonate="chrome",
            timeout=20,
        )
        response.raise_for_status()
        return list(response.json())

    def active_direction(self) -> Direction:
        if self.payload.get(EN_TO_TR.exact_key) or self.payload.get(EN_TO_TR.full_text_key):
            return EN_TO_TR
        if self.payload.get(TR_TO_EN.exact_key) or self.payload.get(TR_TO_EN.full_text_key):
            return TR_TO_EN
        return EN_TO_TR

    def grouped_terms(self, rows: list[dict], direction: Direction) -> OrderedDict[str, list[str]]:
        grouped: OrderedDict[str, list[str]] = OrderedDict()
        seen_by_category: dict[str, set[str]] = {}

        for row in rows:
            category = (row.get("categoryTextA") or row.get("categoryTextB") or "General").strip()
            term = (row.get(direction.target_field) or "").strip()
            if not term:
                continue

            grouped.setdefault(category, [])
            seen_by_category.setdefault(category, set())

            if term in seen_by_category[category]:
                continue

            grouped[category].append(term)
            seen_by_category[category].add(term)

        return grouped

    def fuzzy(self):
        suggestions = self.autocomplete(self.word)
        rprint(", ".join(suggestions))

    def plain(self):
        for category, terms in self.dic.items():
            print(category + ": " + ", ".join(terms))

    def rich(self):
        table = Table(
            show_header=False,
            box=box.SQUARE,
            show_lines=False,
            row_styles=("cyan2", ""),
        )
        table.add_column(justify="right")
        table.add_column()
        for category, terms in self.dic.items():
            table.add_row(category, ", ".join(terms))
        rprint(table)
        Console().print(
            "[grey42][link={}]tureng.com↗[/link]".format(TURENG_URL.format(term=quote(self.word))),
            justify="right",
        )

    @staticmethod
    def render_detailed_table(title: str, rows: list[dict], direction: Direction):
        table = Table(
            title=title,
            show_header=True,
            box=box.SQUARE,
            show_lines=False,
            row_styles=("medium_spring_green", "cyan"),
            expand=True,
        )
        table.add_column("Category", justify="right")
        table.add_column(direction.source_label)
        table.add_column(direction.target_label)

        for row in rows:
            source = (row.get(direction.source_field) or "").strip()
            target = (row.get(direction.target_field) or "").strip()
            category = (row.get("categoryTextA") or row.get("categoryTextB") or "General").strip()
            if source and target:
                table.add_row(category, source, target)

        Console().print(table)

    def detailed(self, direction: Direction):
        exact_rows = self.payload.get(direction.exact_key) or []
        full_text_rows = self.payload.get(direction.full_text_key) or []

        if exact_rows:
            self.render_detailed_table("Exact Results", exact_rows, direction)
        if full_text_rows:
            self.render_detailed_table("Full Text Results", full_text_rows, direction)

        Console().print(
            "[grey42][link={}]tureng.com↗[/link]".format(TURENG_URL.format(term=quote(self.word))),
            justify="right",
        )

    def main(self):
        direction = self.active_direction()
        exact_rows = self.payload.get(direction.exact_key) or []
        full_text_rows = self.payload.get(direction.full_text_key) or []
        suggestions = self.payload.get("suggestions") or self.autocomplete(self.word)

        if not exact_rows and not full_text_rows:
            if self.args.correct and suggestions:
                Console().print(f"Auto-correcting: {self.word} -> {suggestions[0]}\n")
                TurengDict(suggestions[0], self.args)
                return

            print("Not found. Try these:")
            print(", ".join(suggestions) if suggestions else "(no suggestions)")
            raise SystemExit(1)

        self.dic = self.grouped_terms(exact_rows or full_text_rows, direction)

        if self.args.plain:
            self.plain()
        elif self.args.detailed:
            self.detailed(direction)
        else:
            self.rich()
