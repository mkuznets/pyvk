#!/usr/bin/env python3

import ast


def p_spec(p):
    '''
    spec : class_list
    '''
    p[0] = ast.File(p[1])


def p_class_list(p):
    '''
    class_list : class
               | class_list class
    '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]


def p_class(p):
    '''
    class : ID plain_opt LBRACKET attr_list RBRACKET
    '''
    p[0] = ast.Class(p[1], p[2], p[4])


def p_plain_opt(p):
    '''
    plain_opt : CARET
              | empty
    '''
    p[0] = 1 if p[1] else 0


def p_attr_list(p):
    '''
    attr_list : attr
              | attr_list COMMA attr
    '''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_attr(p):
    '''
    attr : ID type_opt required_opt ID
    '''
    p[0] = ast.Attr(*list(p)[1:])


def p_type_opt(p):
    '''
    type_opt : empty
             | STAR
             | STAR STAR
    '''
    p[0] = (1 if p[1] else 0) if len(p) == 2 else 2


def p_required_opt(p):
    '''
    required_opt : empty
                 | BANG
    '''
    p[0] = True if p[1] else False


def p_empty(p):
    'empty :'
    p[0] = ''


def p_error(p):
    if p:
        raise SyntaxError('Syntax error at line %s: `%s\'' % (p.lineno, p.value))
    else:
        raise SyntaxError('Syntax error at EOF')


def build():

    import os
    import lexer
    import ply.yacc as yacc

    tokens = lexer.tokens
    tab_path = os.path.dirname(os.path.realpath(__file__)) + '/~parsetab/spec'
    return yacc.yacc(start='spec', debug=0, tabmodule=tab_path)



import sys
import inspect

def print_grammar():
    rules = []

    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and name[:2] == 'p_'\
                and obj.__doc__ is not None:
            rule = str(obj.__doc__).strip()
            rules.append(rule)

    print("\n".join(rules))


if __name__ == '__main__':
    print_grammar()
