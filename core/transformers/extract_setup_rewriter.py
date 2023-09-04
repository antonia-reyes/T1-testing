from _ast import FunctionDef
from ast import *
import ast
from typing import Any
from core.rewriter import RewriterCommand


class DuplicatedSetupVisitor(NodeVisitor):
    #  Implementar Clase
    def __init__(self):
        super().__init__()
        self.methods = {}
        self.base = []
        self.nodes = []

    def visit_FunctionDef(self, node: FunctionDef):
        self.methods[node.name] = []
        # print(node.body)
        for n in node.body:
            # print('NODE')
            # print(type(n))
            self.nodes.append(n)
            if type(n) is ast.Assign:
                # print(n.targets[0].id)
                # print(n.value.value)
                print(type(n.value))
                if type(n.value) is ast.Constant:
                    self.methods[node.name].append([n.targets[0].id, n.value.value])
                elif type(n.value) is ast.Call:
                    print(n.value.func.id)
                    info = [n.value.func.id]
                    print(n.value.args)
                    for a in n.value.args:
                        info.append(a.value)
                    self.methods[node.name].append(info)
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
        # print('METODOS')
        # print(self.methods)

    def check(self):
        # print(self.methods)
        primero = True
        for m in self.methods.keys():
            if primero:
                self.base = self.methods[m]
                # print(self.base)
                primero = False
            else:
                nueva = []
                for i in range(len(self.base)):
                    if self.base[i] in self.methods[m]:
                        nueva.append(self.base[i])
                    else:
                        break
                self.base = nueva
        # print(self.base)
        self.nodes = self.nodes[:len(self.base)]
        # print(self.nodes)
        # for i in self.nodes:
        #     print(i.targets[0].id)
        return self.nodes
        # if len(self.base) > 0:
        #     self.addWarning('DuplicatedSetup', len(base), f'there are {len(base)} duplicated setup statements')

class SetupTransformer(NodeTransformer):
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes
        self.new_attr = []
        self.setup = False

    def visit_ClassDef(self, node: ClassDef):
        # print('NODOS A CAMBIAR')
        # print(self.nodes)
        # for i in self.nodes:
        #     print(i.targets[0].id)
        # print('Body antes')
        # print(node.body)
        # for i in node.body:
        #     print(i.name)
        #     print(i.args.args[0].arg)
        #     print(i.body)
        for n in self.nodes:
            print(type(n))
            if type(n) is ast.Assign:
                if type(n.value) is ast.Constant:
                    print(n.targets[0].id)
                    print(n.value.value)
                    # new = Assign(targets=[Name(id=n.targets[0].id, ctx=Store())], value=Constant(value=n.value.value, kind=None))
                    new = Assign(targets=[Attribute(value=Name(id='self'), attr=n.targets[0].id, ctx=Store())], value=Constant(value=n.value.value, kind=None))
                    self.new_attr.append(new)
                elif type(n.value) is ast.Call:
                    print('CALL')
                    print(n.value.func)
                    print(n.value.func.id)
                    info = []
                    print(n.value.args)
                    for a in n.value.args:
                        info.append(Constant(value=a.value))
                    #     info.append(a.value)
                    print(info)
                    new = Assign(targets=[Attribute(value=Name(id='self'), attr=n.targets[0].id, ctx=Store())], value=Call(func=Name(id=n.value.func.id, ctx=Load()), args=info, keywords=[]))
                    # new = Expr(value=Call(func=Attribute(value=Name(id='self'), attr=n.value.func.id, ctx=Load()), args=[Constant(value=info[1], kind=None)], keywords=[]))
                    self.new_attr.append(new)
        print('NUEVOS ATRIBUTOS')
        print(self.new_attr)  
        if len(self.new_attr) > 0:
            new = FunctionDef(name='setUp', args=arguments(posonlyargs=[], args=[arg(arg='self')], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=self.new_attr, decorator_list=[], returns=None)
            node.body = [new] + node.body
            self.setup = True
        # print('Body despues')
        # print(node.body)

        # for i in node.body:
        #     print(i.name)
        #     print(i.args.args[0].arg)
        #     print(i.body)
        NodeVisitor.generic_visit(self, node)
        print('Body despues de visitar')
        print(node.body)
        for i in node.body:
            print(i.name)
            for n in i.body:
                print(n)
                if type(n) is ast.Expr:
                    print(n.value.func.value)
                    # print(n.args.args[0].arg)
                    # print(i.body[0].value.func)
                    # print(i.body[0].value.args[0].value)
        return node
    
    def visit_FunctionDef(self, node: FunctionDef):
        if self.setup:
            if node.name != 'setUp':
                # print(node.name)
                # print('BODY ANTES')
                # print(node.body)
                new_body = []
                for n in node.body:
                    new_body.append(n)
                    print(type(n))
                    if type(n) is ast.Assign:
                        # print(n.targets[0].id, n.value.value)
                        if type(n.value) is ast.Constant:
                            for i in self.nodes:
                                # print(i.targets[0].id, i.value.value)
                                if n.targets[0].id == i.targets[0].id and n.value.value == i.value.value:
                                    new_body.remove(n)
                        elif type(n.value) is ast.Call:
                            print('CALL')
                            print(n.value.func)
                            print(n.value.func.id)
                            info = []
                            print(n.value.args)
                            for a in n.value.args:
                                info.append(Constant(value=a.value))
                            #     info.append(a.value)
                            print(info)
                            for i in self.nodes:
                                if n.targets[0].id == i.targets[0].id and n.value.func.id == i.value.func.id and n.value.args[0].value == i.value.args[0].value:
                                    new_body.remove(n)
                    # if n not in self.nodes:
                    #     new_body.append(n)
                    elif type(n) is ast.Expr:
                        print('-------- EXPR -------')
                        print(n.value.args)
                        new_args = []
                        for a in n.value.args:
                            print('TIPO ARG --------------------------------------------------')
                            print(type(a))
                            if type(a) is ast.Name:
                                # print(a.id)
                                for i in range(len(self.nodes)):
                                    # print(self.nodes[i].targets[0].id)
                                    if a.id == self.nodes[i].targets[0].id:
                                        # new_body.remove(n)
                                        new_args.append(self.new_attr[i].targets[0])
                                        # break
                                    # else:
                                        # new_args.append(a)
                                    # print('NEW ARGS')
                                    # print(new_args)
                            elif type(a) is ast.Call:
                                print('------------------------------------------')
                                print('CALL en EXPR')
                                print(a.func)
                                print(a.func.value.id)
                                print(a.func.attr)
                                print('NODES')
                                print(self.nodes)
                                for i in range(len(self.nodes)):
                                    print(self.nodes[i].targets[0].id)
                                    print(self.nodes[i].value.func.id)
                                    if a.func.value.id == self.nodes[i].targets[0].id:
                                        # new_body.remove(n)
                                        call_attr = Call(func=Attribute(value=self.new_attr[i].targets[0], attr=a.func.attr, ctx=Load()), args=a.args, keywords=[])
                                        # new_args.append(self.new_attr[i].targets[0])
                                        new_args.append(call_attr)

                                        # break
                                    # else:
                                        # new_args.append(a)
                                    print('NEW ARGS')
                                    print(new_args)
                                print('------------------------------------------')
                            elif type(a) is ast.Constant:
                                new_args.append(a)

                        n.value.args = new_args
                            # elif type(a) is ast.BinOp:
                                # for i in self.nodes:
                                #     if a.left.id == i[1] or a.right.id == i[1]:
                                #         new_body.remove(n)
                node.body = new_body
                print('BODY')
                print(node.body)
        # return node
        else:
            return node


class ExtractSetupCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.
    def apply(self, ast):
        visitor = DuplicatedSetupVisitor()
        visitor.visit(ast)
        nodes = visitor.check()
        transformer = SetupTransformer(nodes)
        new_tree = fix_missing_locations(transformer.visit(ast))
        return new_tree

    @classmethod
    def name(cls):
        return 'extract-setup'
