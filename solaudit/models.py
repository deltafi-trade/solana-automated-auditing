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
        self.invoked_calls = []


class Program:
    def __init__(self) -> None:
        self.algbra_exprs = {}
        self.functions = {}
        self.pub_exprs = {}
        pass

    def handle_function_def(self, s: str, loc: int, tokens: ParseResults) -> None:
        parse_result = tokens.asDict()
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
            if "if_condition" in parse_result:
                func.if_conditions.append(parse_result["if_condition"])

        if "function_call" in parse_result:
            for fc in parse_result["function_call"]:
                func_name = fc[0]
                if "invoke" in func_name and "signed" in func_name:
                    param_list = flatten(fc[1:])
                    program_name = param_list[0].split("::")[0]
                    func.invoked_calls.append(program_name)

        self.functions[function_name] = func

    def handle_algbra_exp(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_assignment_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        # Handle cases like += -=.
        if "operator" in tokens:
            self.algbra_exprs[lineno(loc, s)] = line(loc, s)

    def handle_struct_stat(self, s: str, loc: int, tokens: ParseResults) -> None:
        self.pub_exprs[lineno(loc, s)] = line(loc, s)
