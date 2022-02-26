"""Checkers read data from models and perform semantic & logical checks.."""

from solaudit.models import Program, flatten


def overUnderFlowChecker(program: Program) -> map:
    exprs = {}
    if len(program.algbra_exprs) > 0:
        print("====== Over/Under flow risk detected at below lines =====")
        for line, expr in program.algbra_exprs.items():
            print("line: %d %s" % (line, expr))
            exprs[line] = expr
    return exprs


def missingSignerCheckChecker(program: Program) -> None:
    func_missing_signer_check = []
    for name, func in program.functions.items():
        is_writting_accounts = False
        for assigned_var in func.assigned_vars:
            for account in func.input_accounts:
                if assigned_var.startswith(account) or assigned_var.startswith(
                    account + "."
                ):
                    is_writting_accounts = True
        is_checking_signer = False
        for if_cond in func.if_conditions:
            for account in func.input_accounts:
                if account + ".is_signer" in set(flatten(if_cond)):
                    is_checking_signer = True

        if is_writting_accounts and not is_checking_signer:
            print("Warning: Missing singer check for function %s!" % name)
            func_missing_signer_check.append(name)

    return func_missing_signer_check


def account_confusions_checker(program: Program) -> map:
    exprs = {}
    if len(program.pub_exprs) > 1:
        print(
            "====== Warning: potential account confusions are detected for below struct definitions ====="
        )
        for line, expr in program.pub_exprs.items():
            print("line: %d %s" % (line, expr))
            exprs[line] = expr
    return exprs


def missing_rent_exempt_checker(program: Program) -> None:
    func_missing_rent_exempt_check = []
    for name, func in program.functions.items():
        for account in func.rent_accounts:
            # check if this rent account has rent exempt check
            is_rent_exempt_checked = False
            for if_cond in func.if_conditions:
                if account + ".is_exempt" in set(flatten(if_cond)):
                    is_rent_exempt_checked = True

            if not is_rent_exempt_checked:
                print(
                    "Warning: Missing rent exempt check for account '%s' in function %s()!"
                    % (account, name)
                )
                func_missing_rent_exempt_check.append(name)

    return func_missing_rent_exempt_check


def missing_ownership_checker(program: Program) -> None:
    func_missing_ownership_check = []
    for name, func in program.functions.items():
        print(func.parameters)
        for account in func.config_accounts:
            is_ownership_checked = False
            for if_cond in func.if_conditions:
                if "&Pubkey" in func.parameters:
                    program_id = func.parameters["&Pubkey"]
                    if account + ".owner != " + program_id in " ".join(
                        flatten(if_cond)
                    ):
                        is_ownership_checked = True

            if not is_ownership_checked:
                print(
                    "Warning: Missing ownership check for account '%s' in function %s()!"
                    % (account, name)
                )
                func_missing_ownership_check.append(name)

    return func_missing_ownership_check


CHECKERS = [
    overUnderFlowChecker,
    missingSignerCheckChecker,
    account_confusions_checker,
    missing_rent_exempt_checker,
    missing_ownership_checker,
]
