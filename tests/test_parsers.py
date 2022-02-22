from solaudit.parsers import *
from solaudit.models import Program


def test_comment():
    """Test parsing comment."""
    content = "This is a comment"
    assert comment.parseString("//" + content).asDict()["comment"] == content


def test_name():
    """Test parsing names."""
    assert name.parseString("abc")[0] == "abc"
    assert name.parseString("abc123")[0] == "abc123"
    assert name.parseString("abc_123")[0] == "abc_123"
    assert name.parseString("abc.def")[0] == "abc.def"
    assert name.parseString("abc::def")[0] == "abc::def"


def test_statement():
    """Test parsing statement."""
    assign_statement_1 = "let a = b + c;"
    assign_statement_2 = "let a: A = b + c;"
    assign_statement_3 = "a += b + c;"
    if_statement = """
        if a > b {
            c = a;
        }
    """
    function_call_statement = "abc(1, 2, 3)"
    function_def_statement = """
        fn test(program_id: &Pubkey, accounts: &[AccountInfo], amount: u32) -> ProgramResult {            
            if a + b > 0 {
                let c = 1;
            }
            let d = 2;

            Ok(())
        }
    """
    return_statement = "return a;"
    program_parser = getProgramParser(Program())
    program_parser.ignore(comment)
    assert (
        len(program_parser.parseString(assign_statement_1).asDict()["assignment_stat"])
        == 1
    )
    assert (
        len(program_parser.parseString(assign_statement_2).asDict()["assignment_stat"])
        == 1
    )
    assert (
        len(program_parser.parseString(assign_statement_3).asDict()["assignment_stat"])
        == 1
    )
    assert len(program_parser.parseString(if_statement).asDict()["if_stat"]) == 1
    assert (
        len(
            program_parser.parseString(function_call_statement).asDict()[
                "function_call"
            ]
        )
        == 1
    )
    assert (
        len(program_parser.parseString(function_def_statement).asDict()["function_def"])
        == 1
    )
    assert (
        len(program_parser.parseString(return_statement).asDict()["return_stat"]) == 1
    )


def test_file():
    """Test parsing solana file."""
    file_content = """
        // this is a comemnt.
        let a: A = 100;
        fn test(program_id: &Pubkey, accounts: &[AccountInfo], amount: u32) -> ProgramResult {            
            if a + b > 0 {
                let c = 1;
            }
            let d = 2;

            Ok(())
        }
    """
    program_parser = getProgramParser(Program())
    program_parser.ignore(comment)
    assert len(program_parser.parseString(file_content).asDict()) == 3
