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

def accountConfusionsChecker(program: Program) -> map:
    exprs = {}
    if len(program.pub_exprs) > 0:
        print("====== Warning: potential account confusions are detected for below struct definitions =====")
        for line, expr in program.pub_exprs.items():
            print("line: %d %s" % (line, expr))
            exprs[line] = expr
    return exprs

CHECKERS = [overUnderFlowChecker,
			missingSignerCheckChecker,
			accountConfusionsChecker]
