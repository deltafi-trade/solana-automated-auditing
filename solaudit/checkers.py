"""Checkers read data from models and perform semantic & logical checks.."""

from solaudit.models import Program


def overUnderFlowChecker(program: Program) -> map:
    exprs = {}
    if len(program.algbra_exprs) > 0:
        print("====== Over/Under flow risk detected at below lines =====")
        for line, expr in program.algbra_exprs.items():
            print("line: %d %s" % (line, expr))
            exprs[line] = expr
    return exprs


CHECKERS = [overUnderFlowChecker]
