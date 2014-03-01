# Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)


# More indentation included to distinguish this from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Extra indentation is not necessary.
foo = long_function_name(
  var_one, var_two,
  var_three, var_four)

my_list = [
    1, 2, 3,
    4, 5, 6,
    ]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
    )

my_list = [
    1, 2, 3,
    4, 5, 6,
]
result = some_function_that_takes_arguments(
    'a', 'b', 'c',
    'd', 'e', 'f',
)


class Rectangle(Blob):

    def __init__(self, width, height,
                 color='black', emphasis=None, highlight=0):
        if (width == 0 and height == 0 and
                color == 'red' and emphasis == 'strong' or
                highlight > 100):
            raise ValueError("sorry, you lose")
        if width == 0 and height == 0 and (color == 'red' or
                                           emphasis is None):
            raise ValueError("I don't think so -- values are %s, %s" %
                             (width, height))
        Blob.__init__(self, width, height,
                      color, emphasis, highlight)


import os
import sys

from subprocess import Popen, PIPE

import mypkg.sibling
from mypkg import sibling
from mypkg.sibling import example

from . import sibling
from .sibling import example

from myclass import MyClass
from foo.bar.yourclass import YourClass

import myclass
import foo.bar.yourclass


spam(ham[1], {eggs: 2})

# Omitted, since it is only in the PEP to show that if you *do*
# use a semi-colon, it shouldn't have a space before it
# The admonition to avoid using semi-colons stands despite the example
# if x == 4: print x, y; x, y = y, x

spam(1)

dict['key'] = list[index]

x = 1
y = 2
long_variable = 3

i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)


def complex(real, imag=0.0):
    return magic(r=real, i=imag)


if foo == 'blah':
    do_blah_thing()
do_one()
do_two()
do_three()

x = x + 1                 # Compensate for border


def f(x): return 2*x

try:
    import platform_specific_module
except ImportError:
    platform_specific_module = None

try:
    process_data()
except Exception as exc:
    raise DataProcessingFailedError(str(exc))

try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)


with conn.begin_transaction():
    do_stuff_in_transaction(conn)

if foo.startswith('bar'):
    pass

if isinstance(obj, int):
    pass
