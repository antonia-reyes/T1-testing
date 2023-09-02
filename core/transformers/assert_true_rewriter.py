from ast import *
import ast
from core.rewriter import RewriterCommand

class AssertTrueTransformer(NodeTransformer):
    def visit_Call(self, node):
        condiciones = isinstance(node.func, Attribute) and isinstance(node.func.value, Name) and node.func.value.id == 'self' and isinstance(node.func.attr, str) and node.func.attr == 'assertEquals'
        if condiciones:
            if isinstance(node.args[0], Constant):
                if node.args[0].value == True:
                    return Call(func=Attribute(value=Name(id='self'), attr='assertTrue', ctx=Load()), args=[node.args[1]], keywords=node.keywords)          
            elif isinstance(node.args[1], Constant):
                if node.args[1].value == True:
                    return Call(func=Attribute(value=Name(id='self'), attr='assertTrue', ctx=Load()), args=[node.args[0]], keywords=node.keywords)
        else:
            return node
class AssertTrueCommand(RewriterCommand):
    # Implementar comando, recuerde que puede necesitar implementar además clases NodeTransformer y/o NodeVisitor.

    def apply(self, ast):
        new_tree = fix_missing_locations(AssertTrueTransformer().visit(ast))
        return new_tree
