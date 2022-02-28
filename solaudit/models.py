"""
Models are used for store informations exracted by parser.
"""

from enum import Enum
from pyparsing import ParseResults, lineno, line

# Signals exposed by the parser.
class Signal(Enum):
    # Statment signals.
    ASSIGNMENT_STAT = "assignment_stat"
    FUNCTION_CALL = "function_call"
    IF_STAT = "if_stat"
    FUNCTION_DEF = "function_def"
    RETURN_STAT = "return_stat"
    STRUCT_STAT = "struct_stat"

    # Variable/name/operator signals.
    FUNCTION_NAME = "function_name"
    ASSIGNED_VAR = "assigned_var"
    OPERATOR = "operator"

    # Expression signals.
    IF_CONDITION = "if_condition"


def flatten(x):
    if isinstance(x, list):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


class Function:
    def __init__(self, name) -> None:
        self.name = name
        self.input_accounts = []
        self.assigned_vars = []
        self.if_conditions = []
        self.rent_accounts = []


class Program:
    def __init__(self) -> None:
        self.algbra_exprs = {}
        self.functions = {}
        self.pub_exprs = {}
        pass

    def handle_function_def(self, s: str, loc: int, tokens: ParseResults) -> None:
        parse_result = tokens.asDict()
        function_name = parse_result[Signal.FUNCTION_NAME.value]
        func = Function(function_name)
        if Signal.ASSIGNMENT_STAT.value in parse_result:
            for stat in parse_result[Signal.ASSIGNMENT_STAT.value]:
                left = stat[0]
                right = flatten(stat[1])
                if "next_account_info" in set(right):
                    func.input_accounts.append(left)
                    if left.casefold() == "rent".casefold():
                        func.rent_accounts.append(left)
                else:
                    func.assigned_vars.append(left)
            if Signal.IF_CONDITION.value in parse_result:
                func.if_conditions.append(parse_result[Signal.IF_CONDITION.value])
        self.functions[function_name] = func

    def handle_algbra_exp(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_assignment_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        # Handle cases like += -=.
        if Signal.OPERATOR.value in tokens:
            self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_struct_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.pub_exprs[lineno(loc, s)] = line(loc, s)
