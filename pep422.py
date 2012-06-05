#!/usr/bin/env python3
# PEP 422 reference implementation

class DynamicDecorators(type):
    """Metaclass for dynamic decorator support

    Creates the class normally, then runs through the MRO looking for
    __decorators__ attributes and applying the contained decorators to
    the newly created class
    """
    def __new__(meta, name, bases, ns):
        cls = super(DynamicDecorators, meta).__new__(meta, name, bases, ns)
        for entry in reversed(cls.mro()):
            decorators = entry.__dict__.get("__decorators__", ())
            for deco in reversed(decorators):
                cls = deco(cls)
        return cls

if __name__ == "__main__":
    # Sanity check for the reference implementation
    def record_call(msg):
        def decorator(cls):
            try:
                history = cls.__dict__["_trace_dynamic"]
            except KeyError:
                history = cls._trace_dynamic = []
            history.append(msg)
            return cls
        return decorator

    class Base(metaclass=DynamicDecorators):
        _registry = []
        def _register(cls, registry=_registry):
            registry.append(cls)
            return cls
        __decorators__ = [_register, record_call("Base")]
        del _register
    print(Base._trace_dynamic)
    assert Base._trace_dynamic == ["Base"]

    class A(Base): pass
    print(A._trace_dynamic)
    assert A._trace_dynamic == ["Base"]
    class B(Base): pass
    print(B._trace_dynamic)
    assert B._trace_dynamic == ["Base"]
        
    class C(B):
        __decorators__ = [record_call("C2"), record_call("C1")]
    print(C._trace_dynamic)
    assert C._trace_dynamic == ["Base", "C1", "C2"]

    class D(A, C):
        __decorators__ = [record_call("D")]
    print(D._trace_dynamic)
    assert D._trace_dynamic == ["Base", "C1", "C2", "D"]

    print(Base._registry)
    assert Base._registry == [Base, A, B, C, D]
