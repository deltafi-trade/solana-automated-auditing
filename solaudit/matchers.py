import pyparsing as pp

ppc = pp.pyparsing_common
pp.ParserElement.enablePackrat()

LBRACK, RBRACK, LBRACE, RBRACE, LPAR, RPAR, EQ, COMMA, SEMI, COLON, REF = map(
    pp.Suppress, "[]{}()=,;:&"
)
RETURN, IF, LET, FN = map(pp.Suppress, ["return", "if", "let", "fn"])

comment = pp.Suppress(pp.Literal("//")) + pp.restOfLine("comment")
string = pp.QuotedString("'") | pp.QuotedString('"')

any_keyword = pp.MatchFirst(RETURN | IF | LET | FN).setName("<keyword>")
ident = ~any_keyword + ppc.identifier("ident")
