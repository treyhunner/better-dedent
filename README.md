# better dedent

[![PyPI - Version](https://img.shields.io/pypi/v/better-dedent.svg)](https://pypi.org/project/better-dedent)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/better-dedent.svg)](https://pypi.org/project/better-dedent)

-----

Like `textwrap.dedent`, but with t-string support.

For example, running this:

```python
code = r"""
def strip_each(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip("\n"))
    return new_lines
""".strip("\n")

text = dedent(t"""\
    Example function:
        {code}

    That function was indented properly!""")
print(text)
```

Would print this:

```
Example function:
    def strip_each(lines):
        new_lines = []
        for line in lines:
            new_lines.append(line.rstrip("\n"))
        return new_lines

That function was indented properly!
```


## Installation

```console
pip install better-dedent
```

## License

`better-dedent` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
