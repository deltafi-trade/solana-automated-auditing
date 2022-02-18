from typing import Mapping
from pyparsing import ParserElement

"""
Define models for parsing results. Example workflow to parse a program file and analyse should look like:
    program = Program(content_to_parse, parser)
    program.parse()

    functions = program.getFunctions()
    for function in functions:
        expr1 = function.get_expression_of_your_interests()
        expr2 = function.get_expression_of_your_interests():
        ....

        # Impement audit check logic
"""


class Expression:
    name: str
    _elements: Mapping(str, str)

    def __init__(self, content: str) -> None:
        self._content = content

    def setElements(self, elements: Mapping(str, str)) -> None:
        self._elements = elements

    def getElements(self) -> Mapping(str, str):
        return self._elements


class Function:
    name: str
    _expressions: Mapping(str, Expression)

    def __init__(self, content) -> None:
        self._content = content

    def setExpressions(self, expressions: Mapping(str, Expression)) -> None:
        self._expressions = expressions

    def getExpressions(self) -> Mapping(str, Expression):
        return self._expressions


class Program:
    name: str
    # TODO: Support use statement, struct if necessary.
    _functions: Mapping(str, Function)
    _parser: ParserElement

    def __init__(self, content: str, parser: ParserElement) -> None:
        self._content = content
        self._parser = parser

    def parse(self) -> bool:
        pass

    def setFunctions(self, functions: Mapping(str, Function)) -> None:
        self._functions = functions

    def getFunctions(self) -> Mapping(str, Function):
        return self._functions


class Project:
    name: str
    _programs: Mapping(str, Program)

    def __init__(self, content) -> None:
        self._content = content

    def parse(self) -> bool:
        # Parse program one-by-one.
        pass

    def setPrograms(self, programs: Mapping(str, Program)) -> None:
        self._programs = programs

    def getPrograms(self) -> Mapping(str, Program):
        return self._programs
