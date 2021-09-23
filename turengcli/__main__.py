from turengcli.cli import TurengDict
import argparse

__version__ = "0.0.2"

# parse arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "word",
    type=str,
    nargs="*",
    help="<word>",
)
ap.add_argument(
    "-d",
    "--detailed",
    action="store_true",
    default=False,
    help="detailed results",
)
ap.add_argument(
    "-p",
    "--plain",
    action="store_true",
    default=False,
    help="returns plain text output",
)
ap.add_argument(
    "-f",
    "--fuzzy",
    action="store_true",
    default=False,
    help="returns fuzzy search results",
)
ap.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
args = ap.parse_args()


def cli():
    word = " ".join(args.word)
    print("Please enter a word.") if word == "" else TurengDict(word, args)


if __name__ == "__main__":
    cli()
