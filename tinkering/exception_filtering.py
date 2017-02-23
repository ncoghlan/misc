"""Uses __subclasscheck__ to filter exception hierarchies"""

# Note https://bugs.python.org/issue12029 keeps this from working with
# actual except clauses, but it works fine with contextlib.suppress and
# other code that calls isinstance() or issubclass() explicitly

class FilteredExceptionMeta(type):
    def __subclasscheck__(cls, other):
        return cls.__subclasshook__(other)
    def __instancecheck__(cls, other):
        return cls.__subclasshook__(type(other))

def filtered_exc(exc_type, *, unless=()):
    class _FilteredException(metaclass=FilteredExceptionMeta):
        @classmethod
        def __subclasshook__(cls, other):
            return (issubclass(other, exc_type)
                    and not issubclass(other, unless))
    return _FilteredException

from contextlib import suppress
selective_filter = suppress(filtered_exc(OSError, unless=FileNotFoundError))
with selective_filter:
    raise OSError("Suppressed")

with selective_filter:
    raise FileNotFoundError("Not suppressed")

