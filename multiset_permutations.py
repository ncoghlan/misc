from collections import Counter
from itertools import permutations

# There are at least three different ways to handle this:
# - mutate a common counter object when recursing
# - generate new Counter objects with "ctr - {k:1}"
# - filter the output of itertools.permutations
#
# This example uses the first approach, inspired by the example given in
# https://mail.python.org/pipermail/python-list/2009-January/521685.html

def _generate_permutations(r, prefix, ctr):
    assert r >= 1
    if len(prefix) == r-1:
        # Actually produce results at this level
        for k, v in sorted(ctr.items()):
            if v:
                yield prefix + (k,)
    else:
        # Adjust the value counts and recurse another level
        for k, v in sorted(ctr.items()):
            if v:
                ctr[k] -= 1
                yield from _generate_permutations(r, prefix+(k,), ctr)
                ctr[k] += 1

def multiset_permutations(iterable, r=None):
    if r is None:
        r = len(iterable)
    elif r > len(iterable):
        return
    if not r:
        yield ()
    else:
        yield from _generate_permutations(r, (), Counter(iterable))

data = "BRR"
list(permutations(set(data)))
list(permutations(data))
list(multiset_permutations(data))

data = "BBBRR"
len(list(permutations(set(data))))
len(list(permutations(data)))
len(list(multiset_permutations(data)))
