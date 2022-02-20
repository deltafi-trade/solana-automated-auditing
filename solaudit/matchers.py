"""
Matchers are used to parse and extract information from code files, these 
information will be stored in models to be used by checkers to implement 
audit logic.
"""

import pyparsing as pp

ppc = pp.pyparsing_common
pp.ParserElement.enablePackrat()

LBRACK, RBRACK, LBRACE, RBRACE, LPAR, RPAR, EQ, COMMA, SEMI, COLON, REF = map(
    pp.Suppress, "[]{}()=,;:&"
)
RETURN, IF, ELSE, LET, FN, TRUE, FALSE = map(
    pp.Suppress, ["return", "if", "else", "let", "fn", "true", "false"]
)
AND, OR, NOT = map(pp.Literal, ["&&", "||", "!"])
OPERATOR = pp.oneOf("+ - * / %")

comment = pp.Suppress(pp.Literal("//")) + pp.restOfLine("comment")
string = pp.QuotedString("'") | pp.QuotedString('"')

any_keyword = pp.MatchFirst(RETURN | IF | LET | FN).setName("<keyword>")
ident = ~any_keyword + ppc.identifier("ident")
name = pp.delimitedList(ident, delim=".", combine=True)

exp = pp.Forward()
exp_list = pp.delimitedList(exp)

stat = pp.Forward()
block = LBRACE + pp.Group(stat + SEMI)[1, ...] + RBRACE

param = ident + COLON + exp
param_list = pp.delimitedList(param)

func_head = FN + name + pp.Group(LPAR + param_list + RPAR) + pp.Suppress("->") + name
function_def = func_head + block
function_call = name + pp.Group(LPAR + exp_list + RPAR)

var = pp.Forward()
var_atom = function_call | name | LPAR + exp + RPAR | LBRACK + name + RBRACK
index_ref = pp.Group(LBRACK + exp + RBRACK)
var <<= pp.delimitedList(pp.Group(var_atom + index_ref) | var_atom, delim=".")

exp_atom = FALSE | TRUE | ppc.number | string | function_call | var
exp <<= pp.infixNotation(
    exp_atom,
    [
        ("&", 1, pp.opAssoc.RIGHT),
        (OPERATOR, 2, pp.opAssoc.LEFT),
        (pp.oneOf("< > <= >= ~= =="), 2, pp.opAssoc.LEFT),
        (AND, 2, pp.opAssoc.LEFT),
        (OR, 2, pp.opAssoc.LEFT),
    ],
)

assignment_stat = pp.Optional(LET) + var + pp.Optional(OPERATOR) + EQ + exp
if_stat = (
    IF
    + LPAR
    + exp
    + RPAR
    + block
    + pp.Optional(pp.Group(ELSE + IF + LPAR + exp + RPAR)[...])
    + pp.Optional(pp.Group(ELSE + block))
)

stat <<= pp.Group(assignment_stat | function_call | if_stat | function_def)

solana_file = stat[...]
