import functools

def op_or_eq(op, self, other):
   # "a < b or a == b" handles "a <= b"
   # "a > b or a == b" handles "a >= b"
   op_result = op(other)
   if op_result:
     # Short circuit OR, as op is True
     # NotImplemented is also passed back here
     return op_result
   return self.__eq__(other)

def op_or_eq_ignore_not_eq(op, self, other):
    # "a < b or a == b" handles "a <= b"
    # "a > b or a == b" handles "a >= b"
    op_result = op(other)
    if op_result is NotImplemented:
        return self.__eq__(other) or NotImplemented
    if op_result:
        return True
    return self.__eq__(other)

le_from_lt_mine = lambda self, other: op_or_eq(self.__lt__, self, other)
le_from_lt_ignore_not_eq = lambda self, other: op_or_eq_ignore_not_eq(self.__lt__, self, other)

@functools.total_ordering
class TotallyOrderedDuckTypeEquals:
   def __init__(self, value):
       self._value = value
   def __eq__(self, other):
       return self._value == getattr(other, "_value", object())
   def __lt__(self, other):
       if not isinstance(other, TotallyOrderedDuckTypeEquals):
           return NotImplemented
       return self._value < other._value

@functools.total_ordering
class TotallyOrderedEqualsReturnsFalse:
   def __init__(self, value):
       self._value = value
   def __eq__(self, other):
       return (isinstance(other, TotallyOrderedEqualsReturnsFalse)
               and self._value == other._value)
   def __lt__(self, other):
       if not isinstance(other, TotallyOrderedEqualsReturnsFalse):
           return NotImplemented
       return self._value < other._value

@functools.total_ordering
class TotallyOrderedEqualsReturnsNotImplemented:
   def __init__(self, value):
       self._value = value
   def __eq__(self, other):
       if not isinstance(other, TotallyOrderedEqualsReturnsNotImplemented):
           return NotImplemented
       return self._value == other._value
   def __lt__(self, other):
       if not isinstance(other, TotallyOrderedEqualsReturnsNotImplemented):
           return NotImplemented
       return self._value < other._value

duck_1 = TotallyOrderedDuckTypeEquals(1)
duck_2 = TotallyOrderedDuckTypeEquals(2)
false_1 = TotallyOrderedEqualsReturnsFalse(1)
false_2 = TotallyOrderedEqualsReturnsFalse(2)
notimpl_1 = TotallyOrderedEqualsReturnsNotImplemented(1)
notimpl_2 = TotallyOrderedEqualsReturnsNotImplemented(2)

assert all([
    duck_1 < duck_2,
    duck_1 <= duck_2,
    false_1 < false_2,
    false_1 <= false_2,
    notimpl_1 < notimpl_2,
    notimpl_1 <= notimpl_2,
    le_from_lt_mine(duck_1, duck_2),
    le_from_lt_mine(false_1, false_2),
    le_from_lt_mine(notimpl_1, notimpl_2),
    le_from_lt_ignore_not_eq(duck_1, duck_2),
    le_from_lt_ignore_not_eq(false_1, false_2),
    le_from_lt_ignore_not_eq(notimpl_1, notimpl_2),
])

false_1 = TotallyOrderedEqualsReturnsFalse(1)
false_2 = TotallyOrderedEqualsReturnsFalse(2)
notimpl_1 = TotallyOrderedEqualsReturnsNotImplemented(1)
notimpl_2 = TotallyOrderedEqualsReturnsNotImplemented(2)

assert not any([
    false_1 < false_1,
    notimpl_1 < notimpl_1,
])

assert all([
    false_1 <= false_1,
    notimpl_1 <= notimpl_1,
    le_from_lt_mine(duck_1, duck_1),
    le_from_lt_mine(false_1, false_1),
    le_from_lt_mine(notimpl_1, notimpl_1),
    le_from_lt_ignore_not_eq(duck_1, duck_1),
    le_from_lt_ignore_not_eq(false_1, false_1),
    le_from_lt_ignore_not_eq(notimpl_1, notimpl_1),
])

import contextlib
@contextlib.contextmanager
def assertTypeError():
    try:
        yield
    except TypeError:
        return
    assert False, "TypeError not raised"

@contextlib.contextmanager
def assertRuntimeError():
    try:
        yield
    except RuntimeError:
        return
    assert False, "RuntimeError not raised"

with assertTypeError():
    false_1 < 2
with assertTypeError():
    false_1 <= 2
with assertTypeError():
    notimpl_1 < 2
with assertTypeError():
    notimpl_1 <= 2
assert all([
    le_from_lt_mine(duck_1, 1) == NotImplemented,
    le_from_lt_mine(duck_1, 2) == NotImplemented,
    le_from_lt_mine(false_1, 2) == NotImplemented,
    le_from_lt_mine(notimpl_1, 2) == NotImplemented,
    le_from_lt_ignore_not_eq(duck_1, 1) == NotImplemented,
    le_from_lt_ignore_not_eq(duck_1, 2) == NotImplemented,
    le_from_lt_ignore_not_eq(false_1, 2) == NotImplemented,
    le_from_lt_ignore_not_eq(notimpl_1, 2) == NotImplemented,
])

with assertRuntimeError():
    false_1 < notimpl_2
with assertRuntimeError():
    false_1 <= notimpl_2
with assertRuntimeError():
    notimpl_1 < false_2
with assertRuntimeError():
    notimpl_1 <= false_2

class OtherType:
    _value = 1

with assertTypeError():
    duck_1 <= OtherType
assert le_from_lt_mine(duck_1, OtherType) == NotImplemented
assert le_from_lt_ignore_not_eq(duck_1, OtherType) == NotImplemented # True!

assert le_from_lt_ignore_not_eq(duck_1, notimpl_1) == True
assert le_from_lt_mine(duck_1, notimpl_1) == True # Fails!!!

assert all([
    le_from_lt_mine(duck_1, notimpl_1) == True,
    le_from_lt_mine(duck_1, notimpl_2) == NotImplemented,
    le_from_lt_mine(false_1, notimpl_2) == NotImplemented,
    le_from_lt_mine(notimpl_1, false_2) == NotImplemented,
    le_from_lt_ignore_not_eq(duck_1, notimpl_1) == True,
    le_from_lt_ignore_not_eq(duck_1, notimpl_2) == NotImplemented,
    le_from_lt_ignore_not_eq(false_1, notimpl_2) == NotImplemented,
    le_from_lt_ignore_not_eq(notimpl_1, false_2) == NotImplemented,
])
