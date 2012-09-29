{
  "events": [
    {
      "act": "OPEN", 
      "size": [
        58, 
        15
      ], 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.233428955078125
    }, 
    {
      "act": "WRITE", 
      "data": "\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007\u001b[?1034h$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "cat tr", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\t", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.0026531219482421875
    }, 
    {
      "act": "WRITE", 
      "data": "\u0007ace", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "1", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\t", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.002210855484008789
    }, 
    {
      "act": "WRITE", 
      "data": ".py ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.001363992691040039
    }, 
    {
      "act": "WRITE", 
      "data": "try:\r\n    1/0\r\nexcept Exception as exc:\r\n    print(\"{}: {}\".format(exc))\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "~/devel/py3k/python -m trace1", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.04132795333862305
    }, 
    {
      "act": "WRITE", 
      "data": "Traceback (most recent call last):\r\n  File \"./trace1.py\", line 2, in <module>\r\n    1/0\r\nZeroDivisionError: division by zero\r\n\r\nDuring handling of the above exception, another exception occurred:\r\n\r\nTraceback (most recent call last):\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 160, in _run_module_as_main\r\n    \"__main__\", fname, loader, pkg_name)\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 73, in _run_code\r\n    exec(code, run_globals)\r\n  File \"./trace1.py\", line 4, in <module>\r\n    print(\"{}: {}\".format(exc))\r\nIndexError: tuple index out of range\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "cat trace2", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.0018551349639892578
    }, 
    {
      "act": "WRITE", 
      "data": "cat: trace2: No such file or directory\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\u001b", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "[", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "A", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "cat trace2", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": ".py", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.0013210773468017578
    }, 
    {
      "act": "WRITE", 
      "data": "x = {}\r\nattr = \"a\"\r\ntry:\r\n    print(x[attr])\r\nexcept KeyError:\r\n    raise AttributeError(attr)\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "~/devel/py3k/python -m trace2", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.03414011001586914
    }, 
    {
      "act": "WRITE", 
      "data": "Traceback (most recent call last):\r\n  File \"./trace2.py\", line 4, in <module>\r\n    print(x[attr])\r\nKeyError: 'a'\r\n\r\nDuring handling of the above exception, another exception occurred:\r\n\r\nTraceback (most recent call last):\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 160, in _run_module_as_main\r\n    \"__main__\", fname, loader, pkg_name)\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 73, in _run_code\r\n    exec(code, run_globals)\r\n  File \"./trace2.py\", line 6, in <module>\r\n    raise AttributeError(attr)\r\nAttributeError: a\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "cat trace3.py", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.0014379024505615234
    }, 
    {
      "act": "WRITE", 
      "data": "x = {}\r\nattr = \"a\"\r\ntry:\r\n    print(x[attr])\r\nexcept KeyError:\r\n    raise AttributeError(attr) from None\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "~/devel/py3k/python -m trace3", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.03512406349182129
    }, 
    {
      "act": "WRITE", 
      "data": "Traceback (most recent call last):\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 160, in _run_module_as_main\r\n    \"__main__\", fname, loader, pkg_name)\r\n  File \"/home/ncoghlan/devel/py3k/Lib/runpy.py\", line 73, in _run_code\r\n    exec(code, run_globals)\r\n  File \"./trace3.py\", line 6, in <module>\r\n    raise AttributeError(attr) from None\r\nAttributeError: a\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "~/devel/py3k/python", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 0.03513813018798828
    }, 
    {
      "act": "WRITE", 
      "data": "Python 3.3.0rc3+ (default:f1094697d7dc, Sep 29 2012, 04:55:01) \r\n[GCC 4.7.2 20120921 (Red Hat 4.7.2-2)] on linux\r\nType \"help\", \"copyright\", \"credits\" or \"license\" for more information.\r\n\u001b[?1034h>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "def f(a, b, c=10, *, d):", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n... ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "    pass", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n... ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "f()", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\nTraceback (most recent call last):\r\n  File \"<stdin>\", line 1, in <module>\r\nTypeError: f() missing 2 required positional arguments: 'a' and 'b'\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "f(1)", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\nTraceback (most recent call last):\r\n  File \"<stdin>\", line 1, in <module>\r\nTypeError: f() missing 1 required positional argument: 'b'\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "f(b=2)", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\nTraceback (most recent call last):\r\n  File \"<stdin>\", line 1, in <module>\r\nTypeError: f() missing 1 required positional argument: 'a'\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "f(1, 2)", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "Traceback (most recent call last):\r\nf  File \"<stdin>\", line 1, in <module>\r\nTypeError: f() missing 1 required keyword-only argument: 'd'\r\n>>>",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "f(1, 2, d=3)", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE",
      "data": ">>> \r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "import os", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "o", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "os.listdir(\"does not exist\")", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "o", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "Traceback (most recent call last):\r\no  File \"<stdin>\", line 1, in <module>\r\nFileNotFoundError: [Errno 2] No such file or directory: 'does not exist'\r\n>>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "os.listdir(\"/usr/bin/python\")", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\nTraceback (most recent call last):\r\n  File \"<stdin>\", line 1, in <module>\r\nNotADirectoryError: [Errno 20] Not a directory: '/usr/bin/python'\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "os.mkdir(\"/usr/bin/python\")", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\nTraceback (most recent call last):\r\n  File \"<stdin>\", line 1, in <module>\r\nFileExistsError: [Errno 17] File exists: '/usr/bin/python'\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "import faulthandler", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n>>> ", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "import threading", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "faulthandler.dump_traceback_later(10, exit=True)", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "a = threading.Thread(target=lambda: b.start() or b.join())", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "b = threading.Thread(target=lambda: a.join())", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "a.start()", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": ">>> ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "ECHO", 
      "data": "a.join()", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\r", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "PAUSE", 
      "duration": 9.946654081344604
    }, 
    {
      "act": "WRITE", 
      "data": "Timeout (0:00:10)!\r\nThread 0x00007fabb0cd1700:\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 184 in wait\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 743 in join\r\n  File \"<stdin>\", line 1 in <lambda>\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 596 in run\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 639 in _bootstrap_inner\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 616 in _bootstrap\r\n\r\nThread 0x00007fabb14d2700:\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 184 in wait\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 743 in join\r\n  File \"<stdin>\", line 1 in <lambda>\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 596 in run\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 639 in _bootstrap_inner\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 616 in _bootstrap\r\n\r\nThread 0x00007fabb8b47740:\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 184 in wait\r\n  File \"/home/ncoghlan/devel/py3k/Lib/threading.py\", line 743 in join\r\n  File \"<stdin>\", line 1 in <module>\r\n\u001b]0;ncoghlan@lancre:~/devel/misc/talks/2012-pyconindia/py3.3-highlights/demo-js\u0007$ ",
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "READ", 
      "data": "\u0004", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "WRITE", 
      "data": "<Press Enter to close demo>\r\n", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }, 
    {
      "act": "CLOSE", 
      "term": "d1f7b7fd72a44c0e9e3ecf2ebaa5406c"
    }
  ]
}