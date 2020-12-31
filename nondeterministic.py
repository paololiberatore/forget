#!/usr/bin/env python3
#
# test nondeterminism implemented by fork, wait and exit (choose and fail)

import os
import sys

# nondeterminism: choose and fail

def choose(s):
    sys.stdout.flush()
    for i,c in enumerate(s):
        if i == len(s) - 1 or os.fork() == 0:
            return c
        else:
            os.wait()
    else:
        fail()

def fail():
    sys.stdout.flush()
    os._exit(0)

# nondeterministically choose a subject

subject = choose(['I', 'you', 'they'])

# nondeterministically choose a verb

verb = choose(['go', 'wait', 'jump', 'sleep'])

# the following code is executed in a separate branch of execution for each
# combination of subject and verb example: print subject and verb, followed by
# an asterisk if the phrase is longer than 8 characters

phrase = subject + ' ' + verb
if (len(phrase) <= 8):
    print(phrase)
else:
    print(phrase + ' *')

