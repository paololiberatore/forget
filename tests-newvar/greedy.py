analyze(
    'the counterexample in the article',
    {'abcdef->g', 'abcdef->h', 'abc->i', 'def->j'})
print()

f = formula('abc->k', 'def->l', 'kl->g', 'kl->h', 'k->i', 'l->j')
print('but this is shorter:', formulatostring(f), formulasize(f))
print()

import subprocess
print('proof they are common equivalent:')
subprocess.check_call('commonequivalent "abcdef->g abcdef->h abc->i def->j" "abc->k def->l kl->g kl->h k->i l->j"', shell=True)

