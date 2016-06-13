class BrokenCM:
    # Context manager broken like @contextmanager was
    # in http://bugs.python.org/issue27122
    def __init__(self, gen):
        self._gen = gen
    def __enter__(self):
        return next(self._gen)
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            raise RuntimeError("Only for exception handling tests")
        if exc_value is None:
            exc_value = exc_type()
        try:
            self._gen.throw(exc_type, exc_value, exc_tb)
        except RuntimeError:
            # Bug was to re-raise RuntimeError unconditionally
            raise
        except Exception as exc:
            # While other exceptions were correctly checked against
            # the active exception state
            if exc is not exc_value:
                raise

class CustomException(Exception): pass

def gen_replace_exception():
    try:
        yield
    except Exception as exc:
        raise CustomException("Custom message") from exc

def gen_reraise_exception():
    try:
        yield
    except:
        raise

print("Checking with statement: ", end="")
try:
    with BrokenCM(gen_replace_exception()):
        with BrokenCM(gen_reraise_exception()):
            raise RuntimeError("Checking with statements")
except CustomException:
    pass
print("OK")

print("Checking contextlib.ExitStack: ", end="")
import contextlib
try:
    with contextlib.ExitStack() as stack:
        stack.enter_context(BrokenCM(gen_replace_exception()))
        stack.enter_context(BrokenCM(gen_reraise_exception()))
        raise RuntimeError("Checking ExitStack")
except CustomException:
    pass

print("OK")

