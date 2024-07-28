import sys
import os

import pytest

# Add the project root directory to Python's module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.writing.utils import (
    get_words,
    is_sub_bullet_point,
    has_text,
    is_bullet_point,
    is_extra_empty_line,
    get_formatted_line,
)


def test_get_words():
    assert get_words("Hello, world!") == ["hello", "world"]


def test_is_sub_bullet_point():
    assert is_sub_bullet_point("  - Sub-bullet") == True
    assert is_sub_bullet_point("- Not sub-bullet") == False


def test_has_text():
    assert has_text("  Text  ") == True
    assert has_text("   ") == False


def test_is_bullet_point():
    assert is_bullet_point("- Bullet") == True
    assert is_bullet_point("• Bullet") == True
    assert is_bullet_point("Not bullet") == False


def test_is_extra_empty_line():
    assert is_extra_empty_line("", [""]) == True
    assert is_extra_empty_line("", ["Text"]) == False


@pytest.mark.parametrize(
    "line,lines,expected",
    [
        ("# Header", [], None),
        ("- Bullet", [], "- Bullet"),
        ("  - Sub-bullet", [], "  - Sub-bullet"),
        ("Text", [], "- Text"),
        ("", [""], None),
    ],
)
def test_get_formatted_line(line, lines, expected):
    assert get_formatted_line(line, lines) == expected
