# SPDX-FileCopyrightText: 2025-present Trey Hunner
#
# SPDX-License-Identifier: MIT
import pytest
import textwrap
from string.templatelib import Template
from hypothesis import given, strategies as st

from better_dedent import dedent, undent, _convert


class TestDedentWithRegularStrings:
    """Test dedent() function with regular string inputs."""

    def test_dedent_basic_indented_string(self):
        text = textwrap.dedent("""\
            hello
            world""")
        result = dedent(text)
        expected = textwrap.dedent("""\
            hello
            world""")
        assert result == expected

    def test_dedent_mixed_indentation(self):
        text = textwrap.dedent("""\
            line1
                line2
            line3""")
        result = dedent(text)
        expected = textwrap.dedent("""\
            line1
                line2
            line3""")
        assert result == expected

    def test_dedent_no_indentation(self):
        text = "hello\nworld"
        result = dedent(text)
        assert result == "hello\nworld"

    def test_dedent_empty_string(self):
        result = dedent("")
        assert result == ""

    def test_dedent_whitespace_only(self):
        result = dedent("    \n    \n")
        assert result == "\n\n"

    def test_dedent_single_line(self):
        result = dedent("    hello")
        assert result == "hello"

    def test_dedent_tabs_and_spaces(self):
        text = "\t    hello\n\t    world"
        result = dedent(text)
        assert result == "hello\nworld"

    def test_dedent_preserves_relative_indentation(self):
        text = textwrap.dedent("""\
                    def func():
                        return 42""")
        result = dedent(text)
        expected = textwrap.dedent("""\
            def func():
                return 42""")
        assert result == expected

    def test_dedent_compatibility_with_textwrap(self):
        text = textwrap.dedent("""\
                hello
                world
                    nested""")
        assert dedent(text) == textwrap.dedent(text)


class TestDedentWithTStrings:
    """Test dedent() function with t-string Template inputs."""

    def test_dedent_tstring_basic(self):
        name = "world"
        template = t"    hello {name}"
        result = dedent(template)
        expected = "hello world"
        assert result == expected

    def test_dedent_tstring_multiline(self):
        color = "purple"
        size = 3
        template = t"""
            Color: {color}
            Size: {size}
        """
        result = dedent(template)
        expected = textwrap.dedent("""
            Color: purple
            Size: 3
            """)
        assert result == expected

    def test_dedent_tstring_with_format_spec(self):
        from math import tau

        template = t"    tau: {tau:.2f}"
        result = dedent(template)
        expected = "tau: 6.28"
        assert result == expected

    def test_dedent_tstring_with_conversion(self):
        color = "purple"
        template = t"    Color: {color!r}"
        result = dedent(template)
        expected = "Color: 'purple'"
        assert result == expected

    def test_dedent_tstring_preserves_interpolation_indentation(self):
        code = textwrap.dedent("""\
            def func():
                return 42""").strip()
        template = t"""\
            Code:
            {code}
        """
        result = dedent(template)
        expected = textwrap.dedent("""\
            Code:
            def func():
                return 42
            """)
        assert result == expected

    def test_dedent_tstring_multiline_interpolation_indented(self):
        lines = textwrap.dedent("""\
            line1
            line2
            line3""").strip()
        template = t"""\
            Content:
                {lines}
        """
        result = dedent(template)
        expected = textwrap.dedent("""\
            Content:
                line1
                line2
                line3
            """)
        assert result == expected

    def test_dedent_tstring_mixed_content(self):
        header = "Header"
        body = textwrap.dedent("""\
            First line
            Second line""").strip()
        template = t"""\
            {header}:
                {body}
                End
        """
        result = dedent(template)
        expected = textwrap.dedent("""\
            Header:
                First line
                Second line
                End
            """)
        assert result == expected

    def test_dedent_tstring_literal_braces(self):
        value = "test"
        template = t"    {{0}} {value}"
        result = dedent(template)
        expected = "{0} test"
        assert result == expected

    def test_dedent_tstring_empty_interpolation(self):
        empty = ""
        template = t"    Value: '{empty}'"
        result = dedent(template)
        expected = "Value: ''"
        assert result == expected

    def test_dedent_tstring_multiple_interpolations_same_line(self):
        x, y = 1, 2
        template = t"    Point: ({x}, {y})"
        result = dedent(template)
        expected = "Point: (1, 2)"
        assert result == expected


class TestUndent:
    """Test undent() function."""

    def test_undent_basic(self):
        text = "\n    hello\n    world\n"
        result = undent(text)
        assert result == "hello\nworld"

    def test_undent_no_leading_newline(self):
        text = "    hello\n    world\n"
        result = undent(text)
        assert result == "hello\nworld"

    def test_undent_no_trailing_newline(self):
        text = "\n    hello\n    world"
        result = undent(text)
        assert result == "hello\nworld"

    def test_undent_preserve_trailing_newline(self):
        text = "\n    hello\n    world\n"
        result = undent(text, strip_trailing=False)
        assert result == "hello\nworld\n"

    def test_undent_with_tstring(self):
        name = "test"
        template = t"\n    Hello {name}\n"
        result = undent(template)
        assert result == "Hello test"

    def test_undent_empty_string(self):
        result = undent("")
        assert result == ""

    def test_undent_only_newlines(self):
        result = undent("\n\n")
        assert result == ""

    def test_undent_whitespace_only(self):
        result = undent("\n    \n    \n")
        assert result == "\n"


class TestConvertHelper:
    """Test _convert() helper function."""

    def test_convert_no_conversion(self):
        assert _convert("hello", None) == "hello"
        assert _convert(42, None) == 42

    def test_convert_str(self):
        assert _convert(42, "s") == "42"
        assert _convert([1, 2, 3], "s") == "[1, 2, 3]"

    def test_convert_repr(self):
        assert _convert("hello", "r") == "'hello'"
        assert _convert([1, 2, 3], "r") == "[1, 2, 3]"

    def test_convert_ascii(self):
        assert _convert("hello", "a") == "'hello'"
        assert _convert("héllo", "a") == "'h\\xe9llo'"


class TestEdgeCases:
    """Test edge cases and complex scenarios."""

    def test_deeply_nested_indentation(self):
        text = "        " * 5 + "deep"
        result = dedent(text)
        expected = "deep"
        assert result == expected

    def test_mixed_tabs_spaces_complex(self):
        text = "\t    line1\n\t\tline2\n\t    line3"
        result = dedent(text)
        expected = "    line1\n\tline2\n    line3"
        assert result == expected

    def test_tstring_with_nested_quotes(self):
        quote = "He said 'hello'"
        template = t'    Message: "{quote}"'
        result = dedent(template)
        assert result == 'Message: "He said \'hello\'"'

    def test_tstring_with_complex_format_specs(self):
        data = {"name": "Alice", "score": 95.678}
        template = t"    {data['name']:>10} scored {data['score']:8.2f}"
        result = dedent(template)
        assert result == "     Alice scored    95.68"

    def test_very_long_interpolation(self):
        long_text = "x" * 1000
        template = t"    Long: {long_text}"
        result = dedent(template)
        assert result == f"Long: {'x' * 1000}"

    def test_no_indentation_before_replacement(self):
        greeting = "Hello"
        name = "Trey"
        template = t"{greeting}{name}"
        result = dedent(template)
        assert result == "HelloTrey"

    def test_curly_braces_before_replacement(self):
        header = "Header"
        body = textwrap.dedent("""\
            First line
            Second line""").strip()
        template = t"""\
            {header}:
                {{{body}}}
            And
                {{{{{body}}}}}
            End
            False replacement: {{3}}
        """
        result = dedent(template)
        expected = textwrap.dedent("""\
            Header:
                {First line
                Second line}
            And
                {{First line
                Second line}}
            End
            False replacement: {3}
            """)
        assert result == expected

    def test_interpolation_preserves_multiline_indentation_complex(self):
        code = textwrap.dedent(r"""
            def strip_each(lines):
                new_lines = []
                for line in lines:
                    new_lines.append(line.rstrip("\n"))
                return new_lines"""
        ).strip("\n")
        template = t"""\
            Example function:
                {code}

            That function was indented properly!"""
        result = dedent(template)
        expected = textwrap.dedent("""\
            Example function:
                def strip_each(lines):
                    new_lines = []
                    for line in lines:
                        new_lines.append(line.rstrip("\\n"))
                    return new_lines

            That function was indented properly!""").strip()
        assert result == expected


class TestPropertyBasedTests:
    """Property-based tests using Hypothesis."""

    @given(st.text())
    def test_dedent_string_compatibility_with_textwrap(self, text):
        """Property test: dedent(string) should always equal textwrap.dedent(string)."""
        assert dedent(text) == textwrap.dedent(text)

    @given(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Zs", "Cc"), max_codepoint=127
            ),
            min_size=0,
            max_size=1000,
        )
    )
    def test_dedent_whitespace_strings(self, text):
        """Property test: dedent should handle whitespace-only strings correctly."""
        assert dedent(text) == textwrap.dedent(text)

    @given(
        st.lists(
            st.text(
                alphabet=st.characters(blacklist_characters="\n"),
                min_size=0,
                max_size=50,
            ),
            min_size=1,
            max_size=20,
        ).map(lambda lines: "\n".join(lines))
    )
    def test_dedent_multiline_strings(self, text):
        """Property test: dedent should handle multiline strings correctly."""
        assert dedent(text) == textwrap.dedent(text)

    @given(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("Lu", "Ll", "Nd", "Zs"), max_codepoint=127
            ),
            min_size=0,
            max_size=200,
        )
    )
    def test_dedent_alphanumeric_strings(self, text):
        """Property test: dedent should handle alphanumeric strings correctly."""
        assert dedent(text) == textwrap.dedent(text)
