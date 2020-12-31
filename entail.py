#!/usr/bin/env python3
#
# check definite Horn entailment

import itertools
import sys


# print up to a certain level of nesting

maxlevel = 2
def printinfo(level, *s):
    if level <= maxlevel:
        if level > 1:
            print(' ' * (8 * (level - 1) - 1), end = '')
        for e in s:
            if e == '\\nonl':
                break;
            print(e, end = '')
        else:
            print()


# make a formula from a collection of lists

def clause(s):
    if isinstance(s, list):
        return frozenset([frozenset(s)])
    elif '=' in s:
        h = s.split('=')
        return clause(h[0] + '->' + h[1]) | clause(h[1] + '->' + h[0])
    else:
        all = frozenset()
        body = set()
        sign = '-'
        for c in s:
            if c == '>':
                sign = ''
            elif c == '-':
                pass
            elif sign == '-':
                body |= {sign + c}
            else:
                all |= {frozenset(body | {sign + c})}
        return all

def formula(*l):
    return set().union(*{clause(x) for x in l})


# from clause to string

def clausetostring(clause, pretty = True):
    if pretty:
        return ''.join({l[1:] for l in clause if l[0] == '-'}) + '->' + \
               ''.join({l for l in clause if l[0] != '-'})
    else:
        return '(' + ' '.join(clause) + ')'


# from formula to string

def formulatostring(formula, label = None, pretty = True):
    s = label + ' ' if label else ''
    s += ' '.join(clausetostring(c, pretty) for c in formula)
    return s


# print a formula 

def formulaprint(formula, label = None, pretty = True):
    print(formulatostring(formula, label, pretty))


# head and body

def head(c):
    return next((l for l in c if l[0] != '-'))

def body(c):
    return {l[1:] for l in c if l[0] == '-'}

def bodies(f):
    return {frozenset(body(c)) for c in f}


# variable propagation

def propagate(b, f):
    heads = set()
    prev = None
    while b != prev:
        prev = b.copy()
        for c in f:
            if body(c) <= b:
                 b |= {head(c)}
    return b


# entailment

def entail(c, f):
   return head(c) in propagate(body(c), f)



# entailment of commandline arguments

c = clause(sys.argv[1])
f = formula(*sys.argv[2:])
# print(c)
# print(f)
for e in c:
    if not entail(e, f):
        quit(0)
else:
    quit(1)

