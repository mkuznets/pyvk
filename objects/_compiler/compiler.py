#!/usr/bin/env python3

import parser as spec_parser
import lexer as spec_lexer
import ast
import sys
import os

sys.path.insert(0, os.path.dirname(__file__) + '/..')


def join(lines, level=0, **kwargs):
    lines = [(' ' * 4 * level) + s.format(**kwargs) for s in lines]
    return "\n".join(lines)


class Builder(ast.NodeVisitor):

    def __init__(self, types={}):
        self.types = types

    def visit_File(self, node, children):
        classes_code = "\n\n\n".join(children['classes'])

        # Base classes.
        with open('_base_classes.py', 'r') as f:
            base_classes_code = f.read()

        # Field types.
        with open('_field_types.py', 'r') as f:
            types_code = f.read()
            lines = types_code.split("\n")
            types_code = ''

            # Get rid of the docstring.
            doc_flag = False
            for line in lines:
                if line.startswith("'''"):
                    doc_flag = not doc_flag
                    continue

                if not doc_flag:
                    types_code += "%s\n" % line

        with open('base.py', 'w') as f:
            f.write(base_classes_code + "\n\n")
            f.write(classes_code + "\n\n")
            f.write(types_code)

    def visit_Class(self, node, children):

        attr_list = []
        attrs_required = []
        methods = []

        for attr in children['attrs']:
            name, getter, setter, condition, required = attr

            if required:
                attrs_required.append("'%s'" % name)

            attr_list.append("'%s'" % name)

            getter_code = join(getter, 1, name=name)
            condition = condition.format(name=name)
            setter_code = join(setter, 1, name=name, condition=condition,
                               cname=node.name)

            methods += [getter_code, setter_code]

        # Compose attribite tuple within 80-character lines.
        attrs_code = '        self.__attrs__ = ('
        i = len(attrs_code)

        for attr in attr_list:
            item = '%s, ' % attr
            if (i + len(item)) > 80:
                attrs_code = "%s\n        " % attrs_code[:-1]
                i = 8
            attrs_code += item
            i += len(item)

        attrs_code = attrs_code[:-2]  # Trim trailing comma and space.
        attrs_code += ')'

        attrs_required_items = ('[%s]' % ', '.join(attrs_required)) if attrs_required else ''
        attrs_required_code = '        self.__attrs_required__ = set(%s)' % attrs_required_items

        if node.plain:
            # Auxiliary objects that are not supposed to have any methods.
            class_lines = [
                'class {cname}(PlainObject):',
                '',
                '    def __init__(self, **kwargs):',
                attrs_code,
                attrs_required_code,
                '',
                '        super({cname}, self).__init__(**kwargs)',
                '',
                "\n\n".join(methods)
            ]

        else:
            # Fully-fledged VK API objects.
            class_lines = [
                'class {cname}(VKObject):',
                '',
                '    def __init__(self, **kwargs):',
                attrs_code,
                attrs_required_code,
                '',
                '        super({cname}, self).__init__(**kwargs)',
                '',
                "\n\n".join(methods)
            ]

        class_code = join(class_lines, cname=node.name)

        return class_code

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
            '        raise TypeError("{cname}.{name}: cannot set attribute with value"',
            '                        " of type `%s\', `' + node.type + '\' expected" % x.__class__.__name__)'
        ]

        if node.type in self.types:
            condition = 'test_%s(x)' % node.type
        else:
            condition = 'type(x) is %s' % node.type

        return (node.name, getter, setter, condition, node.required)


if __name__ == '__main__':

    import inspect
    import _field_types

    types = {name[5:]: member for name, member in inspect.getmembers(_field_types)
                if inspect.isfunction(member) and name.startswith('test_')}

    lexer = spec_lexer.build()
    parser = spec_parser.build()

    with open('base.cfg', 'r') as f:
        code = f.read()

    spec_ast = parser.parse(code)

    b = Builder(types)
    r = b.traverse(spec_ast)
