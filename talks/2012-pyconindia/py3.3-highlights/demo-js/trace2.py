x = {}
attr = "a"
try:
    print(x[attr])
except KeyError:
    raise AttributeError(attr)
