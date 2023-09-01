from _ast import Assign, Name
from typing import Any
from ..rule import *
import ast
from core.rules.warning import *
import inspect

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.variables = {}
    
    def visit_Assign(self, node: Assign):
        if type(node.value) == Constant:
            print('ASSIGN')
            print('VARAIBLE')
            print(node.targets[0].id)
            print('VALOR')
            print(node.value.value)
            self.variables[node.targets[0].id] = node.value.value
            # NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: Call):
        if type(node.func) is ast.Attribute:
            if type(node.args[0]) is ast.Constant:
                if node.func.attr == 'assertTrue' and node.args[0].value == True:
                    print('assert true detected 1')
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
            else:
                if node.func.attr == 'assertTrue':
                    print('assert true detected 2')
                    if node.args[0].id in self.variables:
                        if self.variables[node.args[0].id] == True:
                            self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        # NodeVisitor.generic_visit(self, node)


class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, ast):
        visitor = AssertionTrueVisitor()
        visitor.visit(ast)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'