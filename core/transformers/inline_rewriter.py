from ast import *
from core.rewriter import RewriterCommand
from _ast import Assign, Name
from typing import Any
import ast
import inspect

class ValueVariableVisitor(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.variables = {}
        self.currentFunction = None

    def visit_FunctionDef(self, node: FunctionDef):
        self.currentFunction = node
        self.variables[self.currentFunction.name] = {}
        self.variables["repetidas"] = {}
        NodeVisitor.generic_visit(self, node)
    
    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Name):
                self.variables["repetidas"][target.id] = 0
                print(target.id) # variable (por ej x   y   z  )
                if isinstance(node.value, BinOp): # caso en que y = x + 2, es binop porq es suma
                    #print(node.value.left.id) # x
                    #print(node.value.right.value) # 2
                    if isinstance(node.value.left, Name): #sacando la variable del dict
                        if node.value.left.id in self.variables[self.currentFunction.name]:
                            self.variables["repetidas"][node.value.left.id] += 1
                            #valor_variable = self.variables[self.currentFunction.name].pop(node.value.left.id)
                            #node.value.left = self.variables[self.currentFunction.name][node.value.left.id][0]
                            self.variables[self.currentFunction.name][target.id] = [node.value, node.lineno]
                    elif isinstance(node.value.right, Name): #sacando la variable del dict
                        
                        if node.value.right.id in self.variables[self.currentFunction.name]:
                            self.variables["repetidas"][node.value.left.id] += 1
                            #valor_variable = self.variables[self.currentFunction.name].pop(node.value.left.id)
                            #node.value.right = self.variables[self.currentFunction.name][node.value.right.id][0]
                            self.variables[self.currentFunction.name][target.id] = [node.value, node.lineno]

                if isinstance(node.value, Constant):
                    self.variables[self.currentFunction.name][node.targets[0].id] = [node.value.value, node.lineno]

                if isinstance(node.value, Call):

                    if isinstance(node.value.func, Name):
                        function_name = node.value.func.id
                        self.variables[self.currentFunction.name][target.id] = [node.value, node.lineno]

    def visit_Call(self, node: Call):
        if type(node.func) is ast.Attribute:
            if type(node.args[0]) is ast.Constant:
                pass
            else:
                if node.args[0].id in self.variables[self.currentFunction.name]:
                    #valor_variable = self.variables[self.currentFunction.name].pop(node.args[0].id)
                    pass

    def check(self):
        return self.variables


class VariableTransformer(NodeTransformer):
    def __init__(self, nodes):
        super().__init__()
        self.variables = nodes

    def visit_Assign(self, node: Assign):
        for target in node.targets:
            if isinstance(target, Name):
                #print(target.id) # variable (por ej x   y   z  )
                llave = list(self.variables.keys())[0]
                if target.id in self.variables[llave] and self.variables["repetidas"][target.id] <= 1:
                    return
            return node
    
    def visit_Name(self, node):
        llave = list(self.variables.keys())[0]
        if isinstance(node, Name) and node.id in self.variables[llave]:
            value = self.variables[llave][node.id][0]
            if isinstance(value, ast.Call):
                node = value
                return node
            elif isinstance(value, ast.BinOp):
                print("here")
                print(self.variables)
                print("here")
                if isinstance(value.left, ast.Name):
                    if value.left.id in self.variables[llave] and self.variables["repetidas"][value.left.id] <= 1:
                        value.left = self.variables[llave][value.left.id][0]
                if isinstance(value.right, ast.Name):
                    if value.right.id in self.variables[llave] and self.variables["repetidas"][value.right.id] <= 1:
                        value.right = self.variables[llave][value.right.id][0]
                return value
            return Constant(value=value, kind=None)
        return node


class InlineCommand(RewriterCommand):

    def apply(self, ast):
        visitor = ValueVariableVisitor()
        visitor.visit(ast)
        nodes = visitor.check()
        print("--------------- VARIABLES -----------------")
        print(nodes)
        print("--------------- VARIABLES -----------------")
        transformer = VariableTransformer(nodes)
        new_tree = fix_missing_locations(transformer.visit(ast))
        return new_tree
