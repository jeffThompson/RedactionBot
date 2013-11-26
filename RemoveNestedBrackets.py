#!/usr/bin/python
#
# REMOVE NESTED BRACKETS
# Jeff Thompson | 2013 | www.jeffreythompson.org
#
# First step (removing nested brackets) via:
# http://stackoverflow.com/q/2010413

import itertools
import re

s = "this [text is [in] multiple [brackets]], and [so] is this [text]."

def removeNestedBrackets(string):
  pieces = []
  d = 0
  level = []
  for c in string:
    if c == '[': d += 1
    level.append(d)
    if c == ']': d -= 1
  for k, g in itertools.groupby(zip(string, level), lambda x: x[1]>0):
    block = list(g)
    if max(d for c, d in block) > 1: continue
    pieces.append(''.join(c for c, d in block))
  return ''.join(pieces)

noNested = removeNestedBrackets(s)
print noNested

noBrackets = re.sub('\[.*?\]', '', noNested)
print noBrackets