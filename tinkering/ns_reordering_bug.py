# Bug where class keys get reordered after creation when replacing values
# See https://gist.github.com/dabeaz/617a5b0542d57e003433 for context

def decorate(func):
    print('Decorating', func.__name__)
    return func

def wrap_methods(cls):
    for name in vars(cls):
        if name.startswith('f_'):
            setattr(cls, name, decorate(getattr(cls, name)))
    return cls

class Meta(type):
    pass

# Uncomment below to try the callable-as-metaclass path
# Meta = lambda *args, **kwds: type(*args, **kwds)

class Spam(metaclass=Meta):
    def f_1(self): pass
    def f_2(self): pass
    def f_3(self): pass
    def f_4(self): pass
    def f_5(self): pass
    def f_6(self): pass
    def f_7(self): pass
    def f_8(self): pass

attributes = list(Spam.__dict__)
print(attributes)

wrap_methods(Spam)

wrapped_attributes = list(Spam.__dict__)
print(wrapped_attributes)

mismatched = attributes != wrapped_attributes
print("Broken = ", mismatched)

if __name__ == "__main__":
    import sys
    sys.exit(mismatched)
