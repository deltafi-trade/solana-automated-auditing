from typing import Dict
from solaudit.matchers import *


def test_comment():
    """Test parsing comment."""
    content = "This is a comment"
    assert comment.parseString("//" + content).asDict()["comment"] == content


def test_identifie():
    """Test parsing identifier."""
    assert ident.parseString("abc").asDict()["ident"] == "abc"
    assert ident.parseString("abc123").asDict()["ident"] == "abc123"
    assert ident.parseString("abc_123").asDict()["ident"] == "abc_123"


def test_expression():
    """Test pasing expression."""
    assert exp.parseString("a + b").asList()[0] == ["a", "+", "b"]
    assert exp.parseString("a > b").asList()[0] == ["a", ">", "b"]
    assert exp.parseString("a && b").asList()[0] == ["a", "&&", "b"]
    assert exp.parseString("a || b").asList()[0] == ["a", "||", "b"]


def test_statement():
    """Test parsing statement."""
    assign_statement_1 = "let a = b + c;"
    assign_statement_2 = "a += b + c;"
    if_statement = """
        if (a + b > 0) {
            c = 1;
        }
    """
    function_call_statement = "abc(1, 2, 3)"
    function_def_statement = """
        fn abc(program_id: &Pubkey, accounts: &[AccountInfo], amount: u32) -> ProgramResult {
            let a = 1;
        }
    """
    assert len(stat.parseString(assign_statement_1).asList()) == 1
    assert len(stat.parseString(assign_statement_2).asList()) == 1
    assert len(stat.parseString(if_statement).asList()) == 1
    assert len(stat.parseString(function_call_statement).asList()) == 1
    assert len(stat.parseString(function_def_statement).asList()) == 1
