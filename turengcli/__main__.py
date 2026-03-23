import argparse
from importlib_metadata import version, metadata
from .cli import TurengDict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "word",
        type=str,
        nargs="*",
        help="<word>",
    )
    parser.add_argument(
        "-c",
        "--correct",
        action="store_true",
        default=False,
        help="auto-correct misspelled input with first suggestion",
    )
    parser.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        default=False,
        help="detailed results",
    )
    parser.add_argument(
        "-p",
        "--plain",
        action="store_true",
        default=False,
        help="returns plain text output",
    )
    parser.add_argument(
        "-f",
        "--fuzzy",
        action="store_true",
        default=False,
        help="returns fuzzy search results",
    )
    parser.add_argument("-v", "--version", action="version", version=f"turengcli {version('turengcli')}")
    return parser


def cli():
    args = build_parser().parse_args()
    word = " ".join(args.word)
    print("Please enter a word.") if word == "" else TurengDict(word, args)


if __name__ == "__main__":
    cli()
