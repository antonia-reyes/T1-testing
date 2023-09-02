from _ast import Call, Attribute, FunctionDef, Expr
from typing import Any
from ..rule import *


class AssertionLessVisitor(WarningNodeVisitor):
    # Implementar Clase
    def __init__(self):
        super().__init__()
        self.assert_present = False
    
    def visit_FunctionDef(self, node: FunctionDef):
        # self.functions[node.name] = node.lineno
        nodes = node.body
        for n in nodes:
            if type(n) is Call:
                print(type(n.func))
                if type(n.func) is Attribute:
                    if 'assert' in n.func.attr:
                        self.assert_present = True
            if type(n) is Expr:
                if type(n.value) is Call:
                    if type(n.value.func) is Attribute:
                        if 'assert' in n.value.func.attr:
                            self.assert_present = True
        if not self.assert_present:
            self.addWarning('AssertionLessWarning', node.lineno, 'it is an assertion less test')
        # NodeVisitor.generic_visit(self, node)


class AssertionLessTestRule(Rule):
    #  Implementar Clase
    def analyze(self, ast):
        visitor = AssertionLessVisitor()
        visitor.visit(ast)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-less'
