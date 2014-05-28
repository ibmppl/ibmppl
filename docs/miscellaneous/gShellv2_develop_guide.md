###gShell v2 Developer's Guide

- `query_map.h`

  * Define class `query_base` with two virtual functions `run()` and `help()`. Each command for operating a graph must derive from the base class and implement the two methods. The former gives the execution of the command and the later the help info. `run()` returns an int as the return status; `help()` outputs a text string.

  * Define class `queryMap` that _maps_ a string (command name) to a class pointer in type of `query_base`, where the command is implemented. It has three methods: `createInstance(cmd)` accepts a cmd name as a string, and _returns_ (not create) the query_base instance that implements the command; `get_query_name(std::vector<std::string>& retnames)` returns all the command in their names; `get_map()` returns the map as a pointer.

  * Define a template `DerivedRegister` derived from `queryMap`, whose constructor inserts a pair that associates a command string to a object pointer of base class `query_base`. This registers a command.

  * Define a macro `REGISTER_QUERY_NAME(NAME, STRNAME)` that registers a command, whoes name is STRNAME and the implementation is an object NAME.

 

  