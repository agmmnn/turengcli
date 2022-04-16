# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests, json
from rich import box
from rich.table import Table
from rich.console import Console
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
        # console = Console(record=True)
        for i in self.dic:
            print(i + ": " + ", ".join(self.dic[i]))
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
        Console().print(
            "[grey42][link=https://tureng.com/tr/turkce-ingilizce/{}]tureng.com↗[/link]".format(
                quote(self.word)
            ),
            justify="right",
        )

    def detailed(self):
        url = "https://tureng.com/tr/turkce-ingilizce/" + self.word
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")
        title = soup.title.text
        table = soup.find_all("table", {"id": "englishResultsTable"})
        result = []
        for idx, i in enumerate(table):
            tr = i.find_all("tr")
            frm_to = (
                i.tr.find("th", class_="c2").text
                + "->"
                + i.tr.find("th", class_="c3").text
            )
            result.append([[frm_to]])
            for j in tr:
                t = j.find_all("td")
                if len(t) > 3:
                    result[idx].append(
                        [t[1].text.strip(), t[2].text.strip(), t[3].text.strip()]
                    )
        h2 = soup.find_all("h2")
        for a, i in enumerate(result):
            for idx, j in enumerate(i):
                if idx == 0:
                    globals()[f"table{a}"] = Table(
                        title=h2[a].text,
                        show_header=True,
                        box=box.SQUARE,
                        show_lines=False,
                        row_styles=("medium_spring_green", "cyan"),
                        expand=True,
                    )
                    globals()[f"table{a}"].add_column("", justify="right")
                    globals()[f"table{a}"].add_column(j[0].split("->")[0])
                    globals()[f"table{a}"].add_column(j[0].split("->")[1])
                else:
                    globals()[f"table{a}"].add_row(j[0], j[1], j[2])
        for s in range(len(result)):
            Console().print(globals()[f"table{s}"])
        Console().print(
            "[grey42][link=https://tureng.com/tr/turkce-ingilizce/{}]tureng.com↗[/link]".format(
                quote(self.word)
            ),
            justify="right",
        )

    def main(self):
        if self.rslt == None:
            if self.args.correct:
                Console().print(
                    "Auto-correcting: {} -> {}\n".format(
                        self.word, self.j["MobileResult"]["Suggestions"][0]
                    )
                )
                TurengDict(self.j["MobileResult"]["Suggestions"][0], self.args)
                exit()
            else:
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
        elif self.args.detailed:
            self.detailed()
        else:
            self.rich()
