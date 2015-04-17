#!/usr/bin/env python3

import parser as spec_parser
import lexer as spec_lexer
import ast
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')


class Indenter(ast.NodeVisitor):

    def visit_File(self, node, children):
        return "\n\n".join(children['classes'])

    def visit_Class(self, node, children):

        reql = lambda attr : 2 if attr.required else 0

        max_len = max(len(attr.type) + attr.modifier + reql(attr)
                      for attr in children['attrs'])

        attrs = []

        for attr in children['attrs']:

            margin = max_len - len(attr.type) - attr.modifier - reql(attr) + 1

            s = '  %s%s%s%s%s' % (attr.type,
                                  '*' * attr.modifier,
                                  ' ' * margin,
                                  '! ' * attr.required,
                                  attr.name)

            attrs.append(s)


        r = ['%s%s [' % (node.name, '^' * node.plain),
             ",\n".join(attrs),
             ']'
        ]

        return "\n".join(r)


    def visit_Attr(self, node, children):
        return node


if __name__ == '__main__':

    lexer = spec_lexer.build()
    parser = spec_parser.build()

    with open('base.cfg', 'r') as f:
        code = f.read()

    spec_ast = parser.parse(code)

    b = Indenter()
    r = b.traverse(spec_ast)

    with open('base.cfg-new', 'w') as f:
        f.write(r)
