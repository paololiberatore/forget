#!/usr/bin/env python3
#

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


# check whether a formula is single-head

def issinglehead(e):
    h = [h for c in e for h in c if h[0] != '-']
    return len(h) == len(set(h))


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


# remove clauses that contain a given variable

def removevar(f, v):
   return {c for c in f if v not in c and '-' + v not in c}


# forget functions

# in the article v is considered a global variable

# singlehead solution: the formula is assumed single-head; the loop over the
# possibile clauses always has a single iteration at most

def bodyreplace(f, r, d, v, l = '# '):
    print(l + 'bodyreplace', '(' + formulatostring(f) + ')', end = '')
    print(settostring(r), settostring(d), settostring(v))
    r1 = r - d - v
    print(l + '  r1:', ' '.join(r1))
    if not r1:
        print(l + 'bodyreplace basecase (no variable to replace)')
        return r - d,set()
    s1 = set()
    e1 = set()
    for y in r1:
        if y in d | e1:
            print(l + '  y=' + y + ' skipped')
            continue
        h = headed(f, y)
        fy = removevar(f, y)
        print(l + '  y:', y)
        print(l + '    fy:', formulatostring(fy))
        print(l + '    clauses:', formulatostring(h))
        for c in h:
            print(l + '    clause:', clausetostring(c))
            s,e = bodyreplace(fy, body(c), d | e1, v, l + '      ')
            if e != None:
                e1 = e1 | e | set({y})
                s1 = s1 | s
                break
        else:
            print(l + 'bodyreplace fail (no recursion succeded)')
            return None,None
    print(l + 'bodyreplace return', end = '')
    print(settostring(r - d - r1 | s1), settostring(e1))
    return r - d - r1 | s1, e1


def forget(f, v):
    if not issinglehead(f):
        print('## WARNING: formula is NOT single-head')
        print('##          some clauses may be missing in the result')
    for c in f:
        if head(c) not in v:
            continue
        print('# clause:', clausetostring(c))
        b = bodyreplace(removevar(f, head(c)), body(c), set(), v)[0]
        if b:
            print(''.join(sorted(b)) + '->' + head(c))


# testing functions

def analyze(e, f, v):
    print('##', e)
    fr = formula(*f)
    print('# f:', formulatostring(fr))
    print('# v:', v)
    forget(fr, v)

def donotanalyze(e, f, v):
    pass


# commandline arguments

if len(sys.argv) <= 1 or sys.argv[1] == '-h':
    if len(sys.argv) <= 1:
        print('no argument')
    print('usage:')
    print('\tforget-singlehead.py [-t] testfile.py')
    print('\tforget-singlehead.py -f variables clause clause...' )
    print('\t\tclause: ab->c, ab=c, abc (= a or b or c)')
elif sys.argv[1] == '-f':
    analyze('cmdline formula', {*sys.argv[3:]}, {*sys.argv[2]})
elif sys.argv[1] == '-t':
    exec(open(sys.argv[2]).read())
else:
    exec(open(sys.argv[1]).read())

