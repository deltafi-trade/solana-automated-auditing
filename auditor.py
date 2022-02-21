# A proof of concept prototype to use pyparsing to parse common rust pitfalls.
# Usage: python3 auditor.py -f FILENAME.

from optparse import OptionParser
from pyparsing import *
from solaudit.checkers import CHECKERS
from solaudit.parsers import getProgramParser, comment
from solaudit.models import Program


LBRACK, RBRACK, LBRACE, RBRACE, LPAR, RPAR, EQ, COMMA, SEMI, COLON, QUESTION = map(
    Suppress, "[]{}()=,;:?"
)


def missingSignerCheck(content: str) -> None:
    identifier = Word(alphanums + "_")

    # Check if fetching account.
    next_account_info = Keyword("next_account_info")
    account_right_expr = ... + next_account_info * 1 + ... + SEMI
    account_assignment = Suppress("let") + identifier + EQ + account_right_expr
    is_fetcing_account = len(account_assignment.searchString(content)) > 0

    # Check if checking signer.
    is_signer = Keyword("is_signer")
    is_checking_signer = len(is_signer.searchString(content)) > 0

    if is_fetcing_account and not is_checking_signer:
        print("Warning: Missing singer check!")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", dest="filename", default="")
    (options, _) = parser.parse_args()

    with open(options.filename, "r") as f:
        content = f.read()
        program = Program()

        parser = getProgramParser(program)
        parser.ignore(comment)
        parser.parseString(content)

        for checker in CHECKERS:
            checker(program)
