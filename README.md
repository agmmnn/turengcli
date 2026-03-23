![screenshot](https://user-images.githubusercontent.com/16024979/135759729-fddf0a5b-d2f6-4606-981b-92c5db778322.png)

<a href="https://pypi.org/project/turengcli/">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/turengcli">
</a>

# turengcli

A command-line interface for [Tureng](https://tureng.com/) with fast lookups, fuzzy search, and rich terminal output.

## Install

Install from PyPI with `uv`:

```bash
uv tool install turengcli
```

Install from a local checkout:

```bash
uv tool install .
```

## Usage

Basic lookup:

```bash
tureng hello
```

Detailed output:

```bash
tureng hello -d
```

Plain output:

```bash
tureng merhaba -p
```

Fuzzy search:

```bash
tureng renas -f
```

Auto-correct the first suggestion:

```bash
tureng corrct -c
```

![detailed results](https://user-images.githubusercontent.com/16024979/135759731-4823b47c-351f-4862-bee9-0f6688c4e32b.png)

## Options

```text
-d, --detailed   Show exact and full-text results in table form
-c, --correct    Retry with the first suggestion when the term is not found
-p, --plain      Print grouped results as plain text
-f, --fuzzy      Return autocomplete suggestions only
-v, --version    Show the installed version
```

## Development

Create the project environment and run the CLI locally:

```bash
uv sync
uv run tureng hello
```

## Dependencies

- [curl-cffi](https://pypi.org/project/curl-cffi/)
- [rich](https://pypi.org/project/rich/)

## License

CC0
