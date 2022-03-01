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
    def __init__(self, name) -> None:
        self.name = name
        self.input_accounts = []
        self.assigned_vars = []
        self.if_conditions = []
        self.rent_accounts = []
        self.writing_accounts = []
        self.parameters = {}


class Program:
    def __init__(self) -> None:
        self.algbra_exprs = {}
        self.functions = {}
        self.pub_exprs = {}
        pass

    def handle_function_def(self, s: str, loc: int, tokens: ParseResults) -> None:
        parse_result = tokens.asDict()
        if "function_name" in parse_result:
            function_name = parse_result["function_name"]
            func = Function(function_name)
            if "assignment_stat" in parse_result:
                for stat in parse_result["assignment_stat"]:
                    left = stat[0]
                    right = flatten(stat[1:])
                    if "next_account_info" in set(right):
                        func.input_accounts.append(left)
                        if left.casefold() == "rent".casefold():
                            func.rent_accounts.append(left)
                    else:
                        func.assigned_vars.append(left)

                    for token in right:
                        if "unpack" in str(token):
                            func.writing_accounts.append(left)

            if "if_condition" in parse_result:
                func.if_conditions.append(parse_result["if_condition"])

            if "function_parameters" in parse_result:
                parameters = parse_result["function_parameters"]
                assert len(parameters) % 2 == 0
                i = 0
                while i < len(parameters) - 1:
                    param_name = parameters[i]
                    param_type = "".join(flatten(parameters[i + 1]))
                    func.parameters[param_type] = param_name
                    i += 2

            self.functions[function_name] = func

    def handle_algbra_exp(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_assignment_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        # Handle cases like += -=.
        if "operator" in tokens:
            self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_struct_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.pub_exprs[lineno(loc, s)] = line(loc, s)
