# A proof of concept prototype to use pyparsing to parse common rust pitfalls.
# Usage: python3 auditor.py -f FILENAME.
# Example: python3 auditor.py -f tests/data/over-under-flow-example.rs

from optparse import OptionParser
from pyparsing import *
from solaudit.checkers import CHECKERS
from solaudit.parsers import getProgramParser, comment
from solaudit.models import Program


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
