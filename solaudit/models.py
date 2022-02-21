"""
Models are used for store informations exracted by parser.
"""

from pyparsing import ParseResults, lineno, line


class Program:
    name: str
    algbra_exprs = {}

    def __init__(self) -> None:
        pass

    def handle_algbra_exp(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_assignment_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        # Handle cases like += -=.
        if "operator" in tokens:
            self.algbra_exprs[lineno(loc, s)] = line(loc, s)
