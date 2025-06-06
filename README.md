# better dedent

[![PyPI - Version](https://img.shields.io/pypi/v/better-dedent.svg)](https://pypi.org/project/better-dedent)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/better-dedent.svg)](https://pypi.org/project/better-dedent)

-----

It's like `textwrap.dedent`, but with added t-string support.


## The problem: interpolating before dedenting

Have you ever used `textwrap.dedent` with an f-string that has newline characters in a replacement field?

For example, given this `code` string (which has `newlines` in it):

```python
code = r"""
def strip_each(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip("\n"))
    return new_lines
""".strip("\n")
```

Using `textwrap.dedent` with an f-string that uses `code` in a replacement field results in very strange indentation:

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
```

The problem is that f-strings immediately interpolate their replacement fields.

That `code` string is injected into the new string before `dedent` has a chance to even look at the string.
By the time `textwrap.dedent` does its dedenting, the weirdness has already happened.


## The solution: interpolating after dedenting

Passing a t-string to the `better_dedent.dedent` function allows the replacement fields to maintain their original indentation level.

Using the same `code` string as before:

```python
code = r"""
def strip_each(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip("\n"))
    return new_lines
""".strip("\n")
```

The `better_dedent.dedent` function will dedent the t-string and *then* inject the replacement field, resulting in much more sensible indentation:

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

Using a t-string allows for dedenting the *whole* string *before* the replacement fields are inserted and *then* inserting the replacement fields.

Note that if an f-string is passed to `better_dedent.dedent`, it will simply delegate to `textwrap.dedent`.


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

Or if you have `uv` installed and you'd like to play with it right now:

```console
uvx --with better-dedent python
```

You can then import `dedent` and `undent` like this:

```python
from better_dedent import dedent, undent
```

And try them out:

```python
code = r"""
def strip_each(lines):
    new_lines = []
    for line in lines:
        new_lines.append(line.rstrip("\n"))
    return new_lines
""".strip("\n")

text = undent(t"""
    Here is some example code:

        {code}

    That indentation worked out nicely!
""")
print(text)
```

## License

`better-dedent` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
