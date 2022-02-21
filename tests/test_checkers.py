from solaudit.checkers import overUnderFlowChecker
from solaudit.models import Program
from solaudit.parsers import getProgramParser


def test_overUnderFlowChecker():
    content = """
        fn test(a: u32, b: u32) -> u32 {
            if a + b > 0 {
                a = b;
                a += b;
            }
            return a;
        }
    """
    program = Program()
    parser = getProgramParser(program)

    parser.parseString(content)

    assert len(overUnderFlowChecker(program)) == 2
