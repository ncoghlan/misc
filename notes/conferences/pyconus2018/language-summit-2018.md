Python Language Summit 2018
===========================



* Subinterpreters


Side conversations
------------------

* Auto-activated application environments
  - pyvenv.cfg currently only located relative to Python interpreter
  - relies on shebang line to associate script with venv
  - more Windows-friendly approach: also locate it relative to sys.path[0]
  - bonus: for scripts within a venv bin directory, the venv will auto-activate
    even when run directly by path
  - locations to check:
    - sys.path[0]
    - sys.path[0]/..
    - sys.path[0]/.venv (maybe?)
    - sys.path[0]/__pylocal__?

