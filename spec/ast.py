#-----------------------------------------------------------------
# ** ATTENTION **
# This code was automatically generated from the file:
# ast/spec_ast.cfg
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


class File(Node):
    def __init__(self, classes, coord=None):
        self.classes = classes
        self.coord = coord

    def children(self, expand=False):
        nodelist = []
        if expand:
            for i, child in enumerate(self.classes or []):
                nodelist.append(("classes[%d]" % i, child))
        else:
            nodelist.append(("classes", list(self.classes) or []))
        return tuple(nodelist)

    attr_names = ()

class Class(Node):
    def __init__(self, name, plain, attrs, coord=None):
        self.name = name
        self.plain = plain
        self.attrs = attrs
        self.coord = coord

    def children(self, expand=False):
        nodelist = []
        if expand:
            for i, child in enumerate(self.attrs or []):
                nodelist.append(("attrs[%d]" % i, child))
        else:
            nodelist.append(("attrs", list(self.attrs) or []))
        return tuple(nodelist)

    attr_names = ('name','plain',)

class Attr(Node):
    def __init__(self, type, modifier, name, coord=None):
        self.type = type
        self.modifier = modifier
        self.name = name
        self.coord = coord

    def children(self, expand=False):
        nodelist = []
        return tuple(nodelist)

    attr_names = ('type','modifier','name',)

