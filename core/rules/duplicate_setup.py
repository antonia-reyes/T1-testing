import ast
from ..rule import *

class DuplicatedSetupVisitor(WarningNodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.methods = {}

    def visit_FunctionDef(self, node: FunctionDef):
        self.methods[node.name] = []
        # print(node.body)
        for n in node.body:
            # print('NODE')
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
                    # print(n.value.args)
                    for a in n.value.args:
                        # print(type(a))
                        if type(a) is ast.Name:
                            # print(a.id)
                            exp.append(a.id)
                        elif type(a) is ast.Constant:
                            # print(a.value)
                            exp.append(a.value)
                        elif type(a) is ast.BinOp:
                            # print('BINOP')
                            # print(a.left.id)
                            # print(a.op)
                            # print(a.right.id)
                            exp.append(a.left.id)
                            exp.append(a.op)
                            exp.append(a.right.id)

                self.methods[node.name].append(exp)

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
