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
RETURN, IF, ELSE, LET, FN, TRUE, FALSE, RETURN = map(
    pp.Suppress, ["return", "if", "else", "let", "fn", "true", "false", "return"]
)
AND, OR, NOT, SCOPE_RES = map(pp.Literal, ["&&", "||", "!", "::"])
OPERATOR = pp.oneOf("+ - * / %")
OPT_SEMI = pp.Optional(SEMI).suppress()

comment = pp.Suppress(pp.Literal("//")) + pp.restOfLine("comment")
string = pp.QuotedString("'") | pp.QuotedString('"')

any_keyword = pp.MatchFirst(RETURN | IF | LET | FN).setName("<keyword>")
ident = ~any_keyword + ppc.identifier("ident")
name = pp.delimitedList(ident, delim=pp.Literal(".") | SCOPE_RES, combine=True)
type_name = pp.Optional("&") + pp.Optional("[") + name + pp.Optional("]")

exp = pp.Forward()
exp_list = pp.delimitedList(exp)

stat = pp.Forward()
block = pp.Group(stat + SEMI)[...] + pp.Group(stat + OPT_SEMI)[...]

param = ident + COLON + type_name
param_list = pp.delimitedList(param)

func_head = (
    FN + name + pp.Group(LPAR + param_list + RPAR) + pp.Suppress("->") + type_name
)
ok_stat = pp.Literal("Ok(())")
function_body = LBRACE + block + pp.Optional(ok_stat + OPT_SEMI) + RBRACE
function_def = func_head + function_body
function_call = name + pp.Group(LPAR + pp.Optional(exp_list) + RPAR)

var = pp.Forward()
var_atom = function_call | name | LPAR + exp + RPAR
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

assignment_stat = (
    pp.Optional(LET)
    + var
    + pp.Optional(pp.Group(COLON + type_name))
    + pp.Optional(OPERATOR)
    + EQ
    + exp
)
if_stat = (
    IF
    + exp
    + LBRACE
    + block
    + RBRACE
    + pp.Optional(pp.Group(ELSE + IF + exp + LBRACE + block + RBRACE)[...])
    + pp.Optional(pp.Group(ELSE + LBRACE + block + RBRACE))
)
return_stat = RETURN + exp + SEMI

stat <<= pp.Group(
    assignment_stat | function_call | if_stat | function_def | comment | return_stat
)

solana_file = pp.Group(stat + SEMI)[...] + pp.Group(stat + OPT_SEMI)[...]


def printInfo(s: str, loc: int, tokens: pp.ParseResults):
    print("===========")
    return "hahaha"


solana_file.setParseAction(printInfo)
