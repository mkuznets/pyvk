#!/usr/bin/env python3

keywords = []

tokens = keywords + [
    'ID', 'LBRACKET', 'RBRACKET', 'COMMA', 'STAR', 'CARET', 'BANG'
]

# Tokens

# net operators
t_CARET         = r'\^'
t_STAR          = r'\*'
t_BANG          = r'\!'
t_COMMA         = r','
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_ignore_COMMENT = r'\#.*'


keywords_map = {k.lower(): k for k in keywords}


def t_ID(t):
    r'[A-Za-z_][\w_]*'
    t.type = keywords_map.get(t.value, 'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

###############################################################################

import ply.lex as lex


def build():
    return lex.lex()
