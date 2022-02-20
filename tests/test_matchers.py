from solaudit.matchers import *


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


def test_expression():
    """Test pasing expression."""
    assert exp.parseString("a + b").asList()[0] == ["a", "+", "b"]
    assert exp.parseString("a > b").asList()[0] == ["a", ">", "b"]
    assert exp.parseString("a && b").asList()[0] == ["a", "&&", "b"]
    assert exp.parseString("a || b").asList()[0] == ["a", "||", "b"]


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
    stat.ignore(comment)
    assert len(stat.parseString(assign_statement_1).asList()) == 1
    assert len(stat.parseString(assign_statement_2).asList()) == 1
    assert len(stat.parseString(assign_statement_3).asList()) == 1
    assert len(stat.parseString(if_statement).asList()) == 1
    assert len(stat.parseString(function_call_statement).asList()) == 1
    assert len(stat.parseString(function_def_statement).asList()) == 1
    assert len(stat.parseString(return_statement).asList()) == 1


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
    solana_file.ignore(comment)
    assert len(solana_file.parseString(file_content)) == 2
