# better dedent

[![PyPI - Version](https://img.shields.io/pypi/v/better-dedent.svg)](https://pypi.org/project/better-dedent)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/better-dedent.svg)](https://pypi.org/project/better-dedent)

-----

Like `textwrap.dedent`, but with t-string support.

For example, given this `code` string:

```python
code = r"""
def strip_each(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip("\n"))
    return new_lines
""".strip("\n")
```

Using the `dedent` function with a t-string that uses `code` in a replacement field would maintain the indentation in a sensible way:

```pycon
>>> print(dedent(t"""\
...     Example function:
...         {code}
... 
...     That function was indented properly!""")
...
Example function:
    def strip_each(lines):
        new_lines = []
        for line in lines:
            new_lines.append(line.rstrip("\n"))
        return new_lines

That function was indented properly!
```

Note that using an f-string would *not* work sensibly:

```pycon
>>> print(dedent(f"""\
...     Example function:
...         {code}
...
...     That function was NOT indented properly!"""))
Example function:
    def strip_each(lines):
new_lines = []
for line in lines:
    new_lines.append(line.rstrip("\n"))
return new_lines

That function was NOT indented properly!
```


## undent

This package also includes an `undent` function, which will strip a leading newline (note the lack of `\` after `t"""`):

```pycon
>>> print(undent(t"""
...     Example function:
...         {code}
...     That function was indented properly!"""))
Example function:
    def strip_each(lines):
        new_lines = []
        for line in lines:
            new_lines.append(line.rstrip("\n"))
        return new_lines
That function was indented properly!
```

The `undent` function will also strips a trailing newline by default:

```pycon
>>> print(undent(t"""
...     Example function:
...         {code}
...     That function was indented properly!
... """))
Example function:
    def strip_each(lines):
        new_lines = []
        for line in lines:
            new_lines.append(line.rstrip("\n"))
        return new_lines
That function was indented properly!
>>> print("Note that there's no blank line above this prompt")
Note that there's no blank line above this prompt
```

Passing `strip_trailing=False` to `undent` will suppress trailing newline removal.


## Installation

```console
pip install better-dedent
```

## License

`better-dedent` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
