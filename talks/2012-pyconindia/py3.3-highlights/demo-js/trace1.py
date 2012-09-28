try:
    1/0
except Exception as exc:
    print("{}: {}".format(exc))
