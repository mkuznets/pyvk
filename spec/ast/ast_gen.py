#!/usr/bin/env python3

#-----------------------------------------------------------------
# _ast_gen.py
#
# Generates the AST Node classes from a specification given in
# a configuration file
#
# The design of this module was inspired by astgen.py from the
# Python 2.5 code-base.
#
# Copyright (C) 2008-2013, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------
import pprint
from string import Template


class ASTCodeGenerator(object):
    def __init__(self, cfg_filename='_sync_ast.cfg'):
        """ Initialize the code generator from a configuration
            file.
        """
        self.cfg_filename = cfg_filename
        self.node_cfg = [NodeCfg(name, contents)
            for (name, contents) in self.parse_cfgfile(cfg_filename)]

    def generate(self, file=None):
        """ Generates the code into file, an open file buffer.
        """
        src = Template(_PROLOGUE_COMMENT).substitute(
            cfg_filename=self.cfg_filename)

        src += _PROLOGUE_CODE
        for node_cfg in self.node_cfg:
            src += node_cfg.generate_source() + '\n\n'

        file.write(src)

    def parse_cfgfile(self, filename):
        """ Parse the configuration file and yield pairs of
            (name, contents) for each node.
        """
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                colon_i = line.find(':')
                lbracket_i = line.find('[')
                rbracket_i = line.find(']')
                if colon_i < 1 or lbracket_i <= colon_i or rbracket_i <= lbracket_i:
                    raise RuntimeError("Invalid line in %s:\n%s\n" % (filename, line))

                name = line[:colon_i]
                val = line[lbracket_i + 1:rbracket_i]
                vallist = [v.strip() for v in val.split(',')] if val else []
                yield name, vallist


class NodeCfg(object):
    """ Node configuration.

        name: node name
        contents: a list of contents - attributes and child nodes
        See comment at the top of the configuration file for details.
    """
    def __init__(self, name, contents):
        self.name = name
        self.all_entries = []
        self.attr = []
        self.child = []
        self.seq_child = []

        for entry in contents:
            clean_entry = entry.rstrip('*')
            self.all_entries.append(clean_entry)

            if entry.endswith('**'):
                self.seq_child.append(clean_entry)
            elif entry.endswith('*'):
                self.child.append(clean_entry)
            else:
                self.attr.append(entry)

    def generate_source(self):
        src = self._gen_init()
        src += '\n' + self._gen_children()
        src += '\n' + self._gen_attr_names()
        return src

    def _gen_init(self):
        src = "class %s(Node):\n" % self.name

        if self.all_entries:
            args = ', '.join(self.all_entries)
            arglist = '(self, %s, coord=None)' % args
        else:
            arglist = '(self, coord=None)'

        src += "    def __init__%s:\n" % arglist

        for name in self.all_entries + ['coord']:
            src += "        self.%s = %s\n" % (name, name)

        return src

    def _gen_children(self):
        src = '    def children(self, expand=False):\n'

        if self.all_entries:
            src += '        nodelist = []\n'

            for child in self.child:
                src += (
                    '        if self.%(child)s is not None:' +
                    ' nodelist.append(("%(child)s", self.%(child)s))\n') % (
                        dict(child=child))

            for seq_child in self.seq_child:
                src += (
                    '        if expand:\n'
                    '            for i, child in enumerate(self.%(child)s or []):\n'
                    '                nodelist.append(("%(child)s[%%d]" %% i, child))\n'
                    '        else:\n'
                    '            nodelist.append(("%(child)s", list(self.%(child)s) or []))\n') % (
                        dict(child=seq_child))

            src += '        return tuple(nodelist)\n'
        else:
            src += '        return ()\n'

        return src

    def _gen_attr_names(self):
        src = "    attr_names = (" + ''.join("%r," % nm for nm in self.attr) + ')'
        return src


_PROLOGUE_COMMENT = \
r'''#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# $cfg_filename
#
# Do not modify it directly. Modify the configuration file and
# run the generator again.
# ** ** *** ** **
#
# Node library for syncroniser AST.
#
# Copyright (C) 2014, Max Kuznetsov
# License: BSD
#-----------------------------------------------------------------

'''

_PROLOGUE_CODE = r'''
import sys


class Node(object):
    """ Abstract base class for AST nodes.
    """
    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children(expand=True):
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)


class NodeVisitor(object):

    def generic_visit(self, node, children):
        pass

    def traverse(self, node):

        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)

        children = {}

        if visitor.__doc__ != 'final':
            # Skip the children

            for c_name, c in node.children():
                if type(c) == list:
                    outcome = [self.traverse(i) for i in c]
                else:
                    outcome = self.traverse(c)

                children[c_name] = outcome

        return visitor(node, children) if visitor else None


'''


if __name__ == "__main__":
    import sys
    ast_gen = ASTCodeGenerator('ast/spec_ast.cfg')
    ast_gen.generate(open('ast.py', 'w'))

