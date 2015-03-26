#!/usr/bin/env python3

import parser as spec_parser
import lexer as spec_lexer
import ast

__ = ' ' * 4

def join(lines, level=0, **kwargs):
    lines = [(' ' * 4 * level) + s.format(**kwargs) for s in lines]
    return "\n".join(lines)


class Builder(ast.NodeVisitor):

    def __init__(self, types={}):
        self.types = types

    def visit_File(self, node, children):
        pass

    def visit_Class(self, node, children):


        attr_list = []
        methods = []

        for attr in children['attrs']:
            name, getter, setter, condition = attr

            attr_list.append("'%s'" % name)

            getter_code = join(getter, 1, name=name)
            condition = condition.format(name=name)
            setter_code = join(setter, 1, name=name, condition=condition)

            methods += [getter_code, setter_code]


        class_lines = [
            'class {name}(VKObject):',
            '',
            '    def __init__(self):',
            '        self.__attrs__ = (%s)' % (', '.join(attr_list)),
            '        super({name}, self).__init__()',
            '',
            "\n\n".join(methods)
        ]

        class_code = join(class_lines, name=node.name)
        print(class_code)

    def visit_Attr(self, node, children):

        getter = [
            '@property',
            'def {name}(self):',
            '    if self._{name} is None:',
            '        self._{name} = self._fetch_field(\'{name}\')',
            '    return self._{name}'
        ]

        setter = [
            '@{name}.setter',
            'def {name}(self, x):',
            '    if {condition}:',
            '        self._{name} = x',
            '    else:',
            '        raise TypeError("Wrong type!")'
        ]

        if node.type in self.types:
            condition = 'test_%s({name})'
        else:
            condition = 'type({name}) is %s' % node.type

        return (node.name, getter, setter, condition)


lexer = spec_lexer.build()
parser = spec_parser.build()

with open('objects.cfg', 'r') as f:
    code = f.read()

spec_ast = parser.parse(code)

spec_ast.show()

b = Builder()
r = b.traverse(spec_ast)
