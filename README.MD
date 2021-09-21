![screenshot](https://raw.githubusercontent.com/agmmnn/turengcli/master/ss.png)

<a href="https://pypi.org/project/turengcli/">
<img alt="PyPI" src="https://img.shields.io/pypi/v/turengcli"></a>

Command-line tool for [tureng.com](https://tureng.com/) with rich output.

```
pip install turengcli
```

```
tureng <word>
```

### Arguments

```python
# -p, --plain returns plain text output
$ tureng -p renascence
> General: uyanış, yeniden doğma
> History: rönesans

# -f, --fuzzy returns fuzzy search results
$ tureng -f renas
> renascence, renascency, renascent, renascible
```
