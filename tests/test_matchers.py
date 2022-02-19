from typing import Dict
from solaudit.matchers import *


def test_comment():
    """Test parsing comment."""
    content = "This is a comment"
    parse_result: Dict = comment.parseString("//" + content).asDict()

    assert parse_result["comment"] == content


def test_ident():
    """Test parsing identifier"""
    parse_result1: Dict = ident.parseString("abc").asDict()
    parse_result2: Dict = ident.parseString("abc123").asDict()
    parse_result3: Dict = ident.parseString("abc_123").asDict()

    assert parse_result1["ident"] == "abc"
    assert parse_result2["ident"] == "abc123"
    assert parse_result3["ident"] == "abc_123"
