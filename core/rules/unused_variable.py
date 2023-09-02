from _ast import Assign, Name
from typing import Any
from ..rule import *
import ast
from core.rules.warning import *
import inspect


class UnusedVariableVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.variables = {}

    # def visit_FunctionDef(self, node):
    # # Reset variables when entering a new function
    #     self.variables = {}


    # def visit_FunctionDef(self, node: FunctionDef):
    #     self.currentFunction = node.name
    #     NodeVisitor.generic_visit(self, node)
    #     self.currentFunction = None
    #     self.variables = {}
    
    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Name):
                print(target.id) # variable (por ej x   y   z  )
                if isinstance(node.value, BinOp): # caso en que y = x + 2, es binop porq es suma
                    print(node.value.left.id) # x
                    print(node.value.right.value) # 2
                    if isinstance(node.value.left, Name): #sacando la variable del dict
                        if node.value.left.id in self.variables:
                            valor_variable = self.variables.pop(node.value.left.id)
                            self.variables[target.id] = [valor_variable[0], node.lineno]
                    if isinstance(node.value.right, Name): #sacando la variable del dict
                        if node.value.right.id in self.variables:
                            valor_variable = self.variables.pop(node.value.left.id)
                            self.variables[target.id] = [valor_variable[0], node.lineno]
                #print(node.value.value)
                if isinstance(node.value, Constant):
                    self.variables[node.targets[0].id] = [node.value.value, node.lineno]
        #print(self.variables)

    def visit_Call(self, node: Call):
        #print(self.variables)
        if type(node.func) is ast.Attribute:
            if type(node.args[0]) is ast.Constant:
                pass
            else:
                if node.args[0].id in self.variables:
                    valor_variable = self.variables.pop(node.args[0].id)
                    self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')


class UnusedVariableTestRule(Rule):
    #  Implementar Clase
    def analyze(self, node):
        visitor = UnusedVariableVisitor()
        visitor.visit(node)
        
        no_usadas = visitor.variables.keys()
        warnings = []
        # print('----------------------------')
        # print(visitor.variables)
        # print('----------------------------')
        for variable in no_usadas:
            line_number = visitor.variables[variable][1]
            message = f'variable {variable} has not been used'
            warnings.append(Warning('UnusedVariable', line_number, message))

        print(warnings)

        return warnings
        
    @classmethod
    def name(cls):
        return 'not-used-variable'
