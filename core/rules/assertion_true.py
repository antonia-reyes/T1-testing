from ..rule import *
import ast
from core.rules.warning import *
import inspect

class AssertionTrueVisitor(WarningNodeVisitor):
    #  Implementar Clase
    # def __init__(self):
    #     pass

    def visit_Call(self, node):
        # ARGUMENTOS DE LLAMADA A FUNCION
        print('ARGS')
        print(node.args[0])
        print(type(node.args[0]))
        # SELF
        print('SELF')
        print(node.func.value.id)
        # NOMBRE DE FUNCION
        print('FUNC')
        print(node.func.attr)
        if type(node.args[0]) is ast.Constant:
            if node.func.attr == 'assertTrue' and node.args[0].value == True:
                print('assert true detected')
                # Get lines of function
                # lines, lineno = inspect.getsourcelines(node.lineno)
                # print(lines)
                # print(lineno)
                # GET LINE OF CALL
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        else:
            if node.func.attr == 'assertTrue':
                print('assert true detected')
                # Get lines of function
                # lines, lineno = inspect.getsourcelines(node.__class__)
                # print(lines)
                # print(lineno)
                # GET LINE OF CALL
                self.addWarning('AssertTrueWarning', node.lineno, 'useless assert true detected')
        NodeVisitor.generic_visit(self, node)


class AssertionTrueTestRule(Rule):
    #  Implementar Clase
    def analyze(self, ast):
        visitor = AssertionTrueVisitor()
        visitor.visit(ast)
        return visitor.warningsList()
        
    @classmethod
    def name(cls):
        return 'assertion-true'