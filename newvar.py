#!/usr/bin/env python3
#

import sys


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


# from set to string

def settostring(set):
     return '{' + ' '.join(set) + '}'


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


# size of a formula, as total occurrencies of variables

def formulasize(a):
    return sum([len(x) for x in a])


# head and body

def head(c):
    return next((l for l in c if l[0] != '-'))

def body(c):
    return {l[1:] for l in c if l[0] == '-'}

def bodies(f):
    return {frozenset(body(c)) for c in f}


# clauses with a given head

def headed(f, h):
    return {c for c in f if head(c) == h}


# remove clauses containing a given variable

def removevar(f, v):
   return {c for c in f if v not in c}


# variables in a formula

def variables(f):
    return {v for c in f for v in {head(c)} | body(c)}


# free variable

def free(f):
    s = variables(f)
    y = ord('a')
    max = 0
    for v in s:
        for x in s:
            o = ord(x) - ord('a')
            if o > max:
                max = o
    return chr(max + 1 + ord('a'))


# replace p with n in clause c

def clausereplace(c, p, n):
    if p.issubset(body(c)):
        m = {'-' + v for v in body(c) if v not in p}
        m |= {'-' + n}
        m |= {head(c)}
        return frozenset(m)
    else:
        return c


# introduce a new variable in place of a set

def newvar(f, p):
    n = free(f)
    b = frozenset({'-' + v for v in p})
    return {clausereplace(c, p, n) for c in f} | {frozenset({n} | b)}


# minimize a formula by introducing new variables

def minimize(f):

    fn = {}
    while fn != f:

        # find best b->n for b=c&d from two clauses c->x, d->x of f
        print('# intersecting two bodies:')
        print('# start:', formulatostring(f), formulasize(f))
        fn = f
        bb = {}
        for c in f:
            if len(c) <= 2:
                continue
            for d in f:
                if c == d:
                    continue
                if len(d) <= 2:
                    continue
                b = body(c) & body(d)
                if len(b) <= 1:
                    continue
                ft = newvar(f, b)
                print('#', ''.join(b), '|', formulatostring(ft), formulasize(ft))
                if formulasize(fn) > formulasize(ft):
                    fn = ft
                    bb = b

        print('# ----------')
        if bb == {}:
            continue

        # iteratively improve b->n to b&c->n, where c->n is in f
        print('# intersecting with other bodies:')
        print('# start:', formulatostring(fn), formulasize(fn))
        fp = {}
        b = bb
        while fn != fp:
            fp = fn
            bb = b
            print('# best:', ''.join(b))
            for c in f:
                if len(c) <= 2:
                    continue
                bc = b & body(c)
                if bc == b:
                    continue
                if len(bc) <= 1:
                    continue
                ft = newvar(f, bc)
                print('#', ''.join(bc), '|', formulatostring(ft), formulasize(ft))
                if formulasize(fn) > formulasize(ft):
                    fn = ft
                    bb = bc
            b = bb

        f = fn
        print('# ==========')
    print(formulatostring(f), formulasize(f))
    return f


# testing function

def analyze(l, c):
    print('##', l)
    f = formula(*c)
    m = minimize(f)

def donotanalyze(l, f):
    pass


# commandline arguments

if len(sys.argv) <= 1 or sys.argv[1] == '-h':
    if len(sys.argv) <= 1:
        print('no argument')
    print('usage:')
    print('\tnewvar.py [-t] testfile.py')
    print('\tnewvar.py -f clause clause...' )
    print('\t\tclause: ab->c, ab=c, abc (= a or b or c)')
elif sys.argv[1] == '-f':
    analyze('cmdline formula', {*sys.argv[2:]})
elif sys.argv[1] == '-t':
    exec(open(sys.argv[2]).read())
else:
    exec(open(sys.argv[1]).read())

