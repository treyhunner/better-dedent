# SPDX-FileCopyrightText: 2025-present Trey Hunner
#
# SPDX-License-Identifier: MIT
"""better_dedent - textwrap.dedent, with sensible t-string support"""

import re
from string import Formatter
import textwrap
from string.templatelib import Interpolation, Template
from typing import Literal

__all__ = ["dedent", "undent"]


def undent(text_or_template: Template, strip_trailing: bool = True) -> str:
    """Dedent and strip leading (and optionally trailing) newline."""
    text = dedent(text_or_template).removeprefix("\n")
    if strip_trailing:
        text = text.removesuffix("\n")
    return text


def dedent(text_or_template: Template) -> str:
    """
    Like textwrap.dedent but handle t-strings sensibly.

    Regular strings dedent as usual, but t-strings ensure the
    interpolated value is inserted only after dedenting.
    """
    if isinstance(text_or_template, Template):
        return _dedent_template(text_or_template)
    else:
        return textwrap.dedent(text_or_template)


# https://discuss.python.org/t/add-convert-function-to-string-templatelib/94569/10
_convert = classmethod(Formatter.convert_field).__get__(Formatter)


_INDENT_BEFORE_REPLACEMENT = re.compile(
    r"""
    ^               # Beginning of string
    ( [ \t]+ )      # Indentation
    .*?             # Any characters after indentation
    (?<! { )        # Previous character must NOT be {
    (?: {{ )*       # Even number of { characters (0, 2, 4, etc.)
    { (\d+) }       # Replacement group {N} where N is an int
    """,
    flags=re.MULTILINE | re.VERBOSE,
)


def _dedent_template(template: Template) -> str:
    replacements = []
    parts = []
    n = 0
    for item in template:
        match item:
            case str() as string:
                # Double-up literal { and } characters for later .format() call
                parts.append(string.replace("{", "{{").replace("}", "}}"))
            case Interpolation(value, _, conversion, format_spec):
                value = _convert(value, conversion)
                value = format(value, format_spec)
                replacements.append(value)
                parts.append("{" + str(n) + "}")
                n += 1
    text = dedent("".join(parts))
    for indentation, n in _INDENT_BEFORE_REPLACEMENT.findall(text):
        n = int(n)
        replacements[n] = textwrap.indent(replacements[n], indentation)
        replacements[n] = replacements[n].removeprefix(indentation)
    return text.format(*replacements)
