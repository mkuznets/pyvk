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
    attr : ID modifier_opt ID
    '''
    p[0] = ast.Attr(*list(p)[1:])


def p_modifier_opt(p):
    '''
    modifier_opt : empty
                 | STAR
                 | STAR STAR
    '''
    p[0] = (1 if p[1] else 0) if len(p) == 2 else 2


def p_empty(p):
    'empty :'
    p[0] = ''


def p_error(p):
    if p:
        print('Syntax error at `%s\'' % p.value, p.lineno, ':', p.lexpos)
    else:
        print('Syntax error at EOF')


def build():

    import os
    import lexer
    import ply.yacc as yacc

    tokens = lexer.tokens
    tab_path = os.path.dirname(os.path.realpath(__file__)) + '/~parsetab/spec'
    return yacc.yacc(start='spec', debug=0, tabmodule=tab_path)
