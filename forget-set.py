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


# convert a pair or set of pairs to string

def pairtostring(p):
    return '(' + ' '.join(p[0]) + ' | ' + ' '.join(p[1]) + ')'

def pairsettostring(s):
    return ' '.join({pairtostring(e) for e in s})


# forget functions

# in the article v is considered a global variable

# set solution: bodyreplace returns a set of pairs (s,e)
# start with {(e1,s1)} = {(0,0)}; for each pair (e1,s1) in this set make a
# recursive call with e1 and c; it returns a (possibly empty) set of pairs; for
# each return pair (s,e) turn (e1,s1) into a separate pair (e1 | e | {y}, s1 |
# s); return the set of these pairs; the case of returning emptyset is treated
# implictly

def bodyreplace(f, r, d, v, l = '# '):
    print(l + 'bodyreplace', '(' + formulatostring(f) + ')', end = '')
    print(settostring(r), settostring(d), settostring(v))
    r1 = r - d - v
    print(l + '  r1:', ' '.join(r1))
    if not r1:
        res = set({(frozenset(r - d),frozenset())})
        print(l + 'bodyreplace basecase', pairsettostring(res))
        return res
    p = set({(frozenset(),frozenset())})
    for y in r1:
        np = set()
        for se in p:
            s1 = se[0]
            e1 = se[1]
            print(l + '  y:', y)
            print(l + '    pair:', pairtostring((s1, e1)))
            if y in d | e1:
                print(l + '    skipped')
                continue
            h = headed(f, y)
            if not h:
                print(l + '    no head')
                print(l + 'bodyreplace fail (no head)')
                return set()
            fy = removevar(f, y)
            print(l + '      fy:', formulatostring(fy))
            print(l + '      clauses:', formulatostring(h))
            for c in h:
                print(l + '        clause ' + clausetostring(c))
                pr = bodyreplace(fy, body(c), d | e1, v, l + '        ')
                for o in pr:
                    np = np | {(s1 | o[0], e1 | o[1] | set({y}))}
            print(l + '      pair set:', pairsettostring(np))
        p = np
    res = frozenset({(frozenset(r - d - r1 | se[0]), frozenset(se[1])) for se in p})
    print(l + 'bodyreplace return', pairsettostring(res))
    return res


def forget(f, v):
    for c in f:
        if head(c) not in v:
            continue
        print('# clause:', clausetostring(c))
        bs = bodyreplace(removevar(f, head(c)), body(c), set(), v)
        for b in bs:
            print(''.join(sorted(b[0])) + '->' + head(c))


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
    print('\tforget-set.py [-t] testfile.py')
    print('\tforget-set.py -f variables clause clause...' )
    print('\t\tclause: ab->c, ab=c, abc (= a or b or c)')
elif sys.argv[1] == '-f':
    analyze('cmdline formula', {*sys.argv[3:]}, {*sys.argv[2]})
elif sys.argv[1] == '-t':
    exec(open(sys.argv[2]).read())
else:
    exec(open(sys.argv[1]).read())

