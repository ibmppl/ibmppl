###gShell v2 Developer's Guide

- `query_map.h`

..* Define query class `query_base` with two virtual functions `run()` and `help()`. Each command for operating a graph shall derive from the base class and implement the two methods. 

..* Define 