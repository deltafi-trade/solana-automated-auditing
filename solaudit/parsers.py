"""
Parsers are used to parse and extract information from code files and store them into models.
"""

import pyparsing as pp

from solaudit.models import Program

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
ident = ~any_keyword + ppc.identifier
name = pp.delimitedList(ident, delim=pp.Literal(".") | SCOPE_RES, combine=True)
type_name = pp.Optional("&") + pp.Optional("[") + name + pp.Optional("]")


def getProgramParser(program: Program) -> pp.ParserElement:
    exp = pp.Forward()
    exp_list = pp.delimitedList(exp)

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
            (OPERATOR, 2, pp.opAssoc.LEFT, program.handle_algbra_exp),
            (pp.oneOf("< > <= >= ~= == !="), 2, pp.opAssoc.LEFT),
            (AND, 2, pp.opAssoc.LEFT),
            (OR, 2, pp.opAssoc.LEFT),
            ("?", 1, pp.opAssoc.LEFT),
        ],
    )

    stat = pp.Forward()
    block = (stat + OPT_SEMI)[...]

    param = ident + COLON + type_name
    param_list = pp.delimitedList(param)

    func_head = (
        FN
        + name("function_name")
        + pp.Group(LPAR + param_list + RPAR)
        + pp.Suppress("->")
        + type_name
    )
    ok_stat = pp.Literal("Ok(())")
    func_body = LBRACE + block + pp.Optional(ok_stat + OPT_SEMI) + RBRACE
    function_def = func_head + func_body
    function_def.setParseAction(program.handle_function_def)

    assignment_stat = (
        pp.Optional(LET)
        + var("assigned_var*")
        + pp.Optional(pp.Group(COLON + type_name))
        + pp.Optional(OPERATOR)
        + EQ
        + exp
    ).setParseAction(program.handle_assignment_stat)
    if_stat = (
        IF
        + exp("if_condition*")
        + LBRACE
        + block
        + RBRACE
        + pp.Optional(pp.Group(ELSE + IF + exp + LBRACE + block + RBRACE)[...])
        + pp.Optional(pp.Group(ELSE + LBRACE + block + RBRACE))
    )
    return_stat = RETURN + exp + SEMI

    stat <<= (
        assignment_stat("assignment_stat*")
        | function_call
        | if_stat
        | function_def("function_def*")
        | comment
        | return_stat
    )

    solana_file = (stat + OPT_SEMI)[...]

    return solana_file
