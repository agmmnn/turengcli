# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import json
from rich.console import Console
from rich.table import Table
from rich import box
from rich import print as rprint


class TurengDict:
    def __init__(self, word, args):
        self.word = word
        self.args = args

        if self.args.fuzzy:
            self.fuzzy()
        else:
            self.req()
            self.main()

    def req(self):
        url = "http://ws.tureng.com/TurengSearchServiceV4.svc/Search"
        payload = {"Term": self.word}
        headers = {"Content-Type": "application/json", "Origin": "tureng.com"}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.j = json.loads(response.text)  # encoding="utf8"
        self.rslt = self.j["MobileResult"]["Results"]

    def fuzzy(self):
        url = "https://ac.tureng.co/?t=" + quote(self.word)
        j = list(json.loads(requests.get(url).content))
        rprint(", ".join(j))

    def plain(self):
        console = Console(record=True)
        for i in self.dic:
            console.print(i + ": " + ", ".join(self.dic[i]))
        # import pyperclip
        # pyperclip.copy(console.export_text())

    def rich(self):
        table = Table(
            show_header=False,
            box=box.SQUARE,
            show_lines=False,
            row_styles=("cyan2", ""),
        )
        table.add_column(justify="right")
        table.add_column()
        for i in self.dic:
            table.add_row(i, ", ".join(self.dic[i]))
        rprint(table)
        rprint(
            "[link=https://tureng.com/tr/turkce-ingilizce/{}]tureng.com↗[/link]".format(
                quote(self.word)
            )
        )

    def main(self):
        if self.rslt == None:
            print("Not found. Try these:")
            print(", ".join(self.j["MobileResult"]["Suggestions"]))
            exit()
        else:
            self.dic = {}
            for i in self.rslt:
                catg = i["CategoryEN"][:-9]
                if catg not in self.dic:
                    self.dic[catg] = [i["Term"]]
                else:
                    self.dic[catg].append(i["Term"])

        if self.args.plain:
            self.plain()
        else:
            self.rich()
