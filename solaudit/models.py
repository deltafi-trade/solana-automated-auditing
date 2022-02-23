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
"""
Models are used for store informations exracted by parser.
"""

from pyparsing import ParseResults, lineno, line


def flatten(x):
    if isinstance(x, list):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]


class Function:
    name: str
    input_accounts = []
    assigned_vars = []
    if_conditions = []

    def __init__(self, name) -> None:
        self.name = name


class Program:
    name: str
    algbra_exprs = {}
    functions = {}

    def __init__(self) -> None:
        pass

    def handle_function_def(self, s: str, loc: int, tokens: ParseResults) -> None:
        parse_result = tokens.asDict()
        function_name = parse_result["function_name"]
        func = Function(function_name)
        if "assignment_stat" in parse_result:
            for stat in parse_result["assignment_stat"]:
                left = stat[0]
                right = flatten(stat[1])
                if "next_account_info" in set(right):
                    func.input_accounts.append(left)
                else:
                    func.assigned_vars.append(left)
            func.if_conditions = parse_result["if_condition"]
        self.functions[function_name] = func

    def handle_algbra_exp(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_assignment_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        # Handle cases like += -=.
        if "operator" in tokens:
            self.algbra_exprs[lineno(loc, s)] = line(loc, s)
