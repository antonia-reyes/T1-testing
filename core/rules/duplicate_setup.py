import ast
from ..rule import *

# class AttributeVisitor(NodeVisitor):
#     def __init__(self):
#         self.nodes = {}

#     def visit_(self, node: FunctionDef):
#         self.functions[node.name] = node.lineno
#         NodeVisitor.generic_visit(self, node)

class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.methods = {}

    def visit_FunctionDef(self, node: FunctionDef):
        self.methods[node.name] = []
        # print(self.methods)
        for n in node.body:
            # print(type(n))
            if type(n) is ast.Assign:
                # print(n.targets[0].id)
                # print(n.value.value)
                self.methods[node.name].append([n.targets[0].id, n.value.value])
            elif type(n) is ast.Expr:
                exp = []
                # print(type(n.value))
                if type(n.value) is ast.Call:
                    exp.append(n.value.func.attr)
                    # print(n.value.func.attr)
                    print(n.value.args)
                    for a in n.value.args:
                        print(type(a))
                        print(a.id)
                        exp.append(a.id)
                # elif type(n.value) is ast.

                self.methods[node.name].append(exp)
                    # print(n.value.args)
            # self.methods[node.name].append([n.])
            # if type(n) is ast.Call:
            #     if type(n.func) is ast.Attribute:
            #         if n.func.attr == 'setUp':
            #             self.methods[node.name].append(n.lineno)
        # print(node.body)
        # visitor = AttributeNodeCounterVisitor()
        # visitor.visit(node)
        # if visitor.total() == 0:
        #     self.addWarning('UncoupledMethodWarning', node.lineno, 'method ' + node.name +
        #                     ' does not use any attribute')
        # NodeVisitor.generic_visit(self, node)
        # print(self.methods)

    def check(self):
        print(self.methods)
        base = []
        primero = True
        for m in self.methods.keys():
            if primero:
                base = self.methods[m]
                print(base)
                primero = False
            else:
                nueva = []
                for i in range(len(base)):
                    if base[i] in self.methods[m]:
                        nueva.append(base[i])
                    else:
                        break
                base = nueva
        print(base)
        if len(base) > 0:
            self.addWarning('DuplicatedSetup', len(base), f'there are {len(base)} duplicated setup statements')

        
    # def visit_Assign(self, node: Assign):
    #     if type(node.value) == Constant:
    #         print('ASSIGN')
    #         print('VARAIBLE')
    #         print(node.targets[0].id)
    #         print('VALOR')
    #         print(node.value.value)
    #         self.variables[node.targets[0].id] = node.value.value
    #         NodeVisitor.generic_visit(self, node)


class DuplicatedSetupRule(Rule):
    #  Implementar Clase
    def analyze(self, ast):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(ast)
        visitor.check()
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'duplicate-setup'
