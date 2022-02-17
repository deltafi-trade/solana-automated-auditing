# A proof of concept prototype to use pyparsing to parse common rust pitfalls.
# Usage: python3 analyzer.py -f FILENAME.

from optparse import OptionParser
from pyparsing import *


LBRACK, RBRACK, LBRACE, RBRACE, LPAR, RPAR, EQ, COMMA, SEMI, COLON, QUESTION = map(
    Suppress, "[]{}()=,;:?"
)


def overUnderFlowCheck(content: str) -> None:
    variable = Word(alphanums)
    arith_op = oneOf("+ - * /")
    equation = variable + arith_op + variable
    equation.ignore(cppStyleComment)

    def printInfo(s: str, loc: int, tokens: ParseResults):
        print(
            "Warning: overflow & underflow at line: %d %s"
            % (lineno(loc, s), line(loc, s))
        )

    equation.setParseAction(printInfo)
    equation.searchString(content)


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

        # do checks
        overUnderFlowCheck(content)
        missingSignerCheck(content)
