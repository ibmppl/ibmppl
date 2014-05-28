###gShell v2 Developer's Guide

- `query_map.h`

  * Define class `query_base` with two virtual functions `run()` and `help()`. Each command for operating a graph shall derive from the base class and implement the two methods. The former gives the execution of the command and the later the help info. `run()` returns an int as the return status; `help()` outputs a text string.

  * Define class `queryMap` that _maps_ a string (command name) to a class pointer in type of `query_base`, where the command is implemented.  