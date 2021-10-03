![screenshot](https://user-images.githubusercontent.com/16024979/135759729-fddf0a5b-d2f6-4606-981b-92c5db778322.png)

<a href="https://pypi.org/project/turengcli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/turengcli"></a>

Command-line tool for [tureng.com](https://tureng.com/) with rich output.

```
pip install turengcli
```

# Usage

```
tureng <word>
```

```
# example usage with -d(detailed results) argument
tureng goner -d
```

![detailed results](https://user-images.githubusercontent.com/16024979/135759731-4823b47c-351f-4862-bee9-0f6688c4e32b.png)

# Arguments

```
# -d, --detailed  detailed results
$ tureng goner -d

# -p, --plain   returns plain text output
$ tureng renascence -p
> General: uyanış, yeniden doğma
> History: rönesans

# -f, --fuzzy   returns fuzzy search results
$ tureng renas -f
> renascence, renascency, renascent, renascible
```

# Requirements

- Python >3.5

## Dependencies

- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [rich](https://pypi.org/project/rich/)
- [lxml](https://pypi.org/project/lxml/)

# License

CC0
