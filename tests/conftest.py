import pytest

from solaudit.models import Program
from solaudit.parsers import getProgramParser, comment


@pytest.fixture
def program():
    return Program()


@pytest.fixture
def parser(program):
    parser = getProgramParser(program)
    parser.ignore(comment)
    return parser
