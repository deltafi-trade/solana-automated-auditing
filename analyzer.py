# A proof of concept prototype to use pyparsing to parse common rust pitfalls.
# Usage: python3 analyzer.py -f FILENAME.

from optparse import OptionParser
from pyparsing import *


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


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", dest="filename", default="")
    (options, _) = parser.parse_args()

    with open(options.filename, "r") as f:
        content = f.read()

        # do checks
        overUnderFlowCheck(content)
