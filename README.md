![screenshot](https://user-images.githubusercontent.com/16024979/135759729-fddf0a5b-d2f6-4606-981b-92c5db778322.png)

<a href="https://pypi.org/project/turengcli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/turengcli"></a>

Command-line tool for [tureng.com](https://tureng.com/) with rich output.

```bash
uv tool install .
```

# Usage

```bash
tureng <word>
```

```bash
# example usage with -d (detailed results) argument
tureng goner -d
```

![detailed results](https://user-images.githubusercontent.com/16024979/135759731-4823b47c-351f-4862-bee9-0f6688c4e32b.png)

# Arguments

```bash
# -d, --detailed  detailed results
tureng goner -d

# -c, --correct   auto-correct misspelled input with first suggestion
tureng corrct -d
# Auto-correcting: corrct -> correct

# -p, --plain   returns plain text output
tureng renascence -p
# General: uyanış, yeniden doğma
# History: rönesans

# -f, --fuzzy   returns fuzzy search results
tureng renas -f
# renascence, renascency, renascent, renascible
```

# Development

```bash
uv sync
uv run tureng hello
```

## Dependencies

- [curl-cffi](https://pypi.org/project/curl-cffi/)
- [rich](https://pypi.org/project/rich/)

# License

CC0
