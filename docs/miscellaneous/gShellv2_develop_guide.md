##gShell v2 Developer's Guide

###Background in gShell v2 Framework

gShell v2 provides an open framework for users to add self-defined commands. Each command in gShell v2 has a corresponding endpoint in the System G Native Store REST APIs.

The follow files can be involved or developers of gShell commands when adding new commands or plug-in analytics tools:

- `types.h`

  * Define `query_arg_type` as type for command arguments, which is essentially a `multimap<string,string>`.

  * Define `graph_type` as the `ibmppl::ibm_generic_graph`

  * Define class `query_param_type` that stores a graph pointer and its associated global properties, including `directness`, `key_to_id`, `id_to_key`, internal_outputFormat, and query_arg_type. 

- `defines.hpp`

  * Define a set of constants for representing argument names and return values.

- `query_map.h`

  * Define class `query_base` with two virtual functions `run()` and `help()`. Each command for operating a graph must derive from the base class and implement the two methods. The former gives the execution of the command and the later the help info. `run()` returns an int as the return status; `help()` outputs a text string.

  * Define class `queryMap` that _maps_ a string (command name) to a class pointer in type of `query_base`, where the command is implemented. It has three methods: `createInstance(cmd)` accepts a cmd name as a string, and _returns_ (not create) the query_base instance that implements the command; `get_query_name(std::vector<std::string>& retnames)` returns all the command in their names; `get_map()` returns the map as a pointer.

  * Define a template `DerivedRegister` derived from `queryMap`, whose constructor inserts a pair that associates a command string to a object pointer of base class `query_base`. This registers a command.

  * Define a macro `REGISTER_QUERY_NAME(NAME, STRNAME)` that registers a command, whoes name is STRNAME and the implementation is an object NAME.

- `nvStore.h / nvStore.cpp`

  * `run_input(string& data, string& cmd, socket_server_type& sock, int mode, simpleShell& shell)` accepts an input from user. The input is obtained using a class `simpleShell`, which supports arrow keys and command/filename auto complete. The user input is stored in `data`. `cmd` is used when gShell is launched in argument mode, where it stores the argument. `sock` is used when gShell is launched in socket mode. 

  * `argument_processs(query_arg_type& args,
                       string& data, string& query_cmd,
                       string& store_name, string& output_name,
                       string& output_format_name)` parses the received argument. The parser is done by `stringParser::argumentParser(data,args,query_cmd);`, where the input `data` is decomposed into `args` and `cmd`. From the args, the input graph store `store_name`, the output variable name `output_name` and the output format are identified. 

  * `store_process(query_arg_type& args, string& query_cmd,
                  string& store_name, internal_outputFormat& i_out,
               store_manager_type& stores)' executes the store management commands in `query_cmd` regarding the specified graph store `store_name`. By store management, we mean `create`, `delete`, `open`, `close`, `close_all`.

  * `run(int mode, string &cmd)` manages multiple graph stores. This function first checks if the command is a store management command and, if so, executes it in `int ret = store_process(args,query_cmd,store_name,i_out,stores);`. If not, it should be a store query, which is executed in `ret = execute(store_ptr, args, query_cmd);` 

  * ` struct sigaction sigIntHandler;` handles ctrl-C during execution.
 
-----------------

### Handon example on how to add new command

- add a global command (e.g., `create`, `list_all`, etc.)

  * add the global command in `nvStore.cpp::store_process()`.
  
  * add the global command help info to `init_command_parser()`.

  * all argument names of a commnad should be defined in `defines.hpp`

  * output should be assigned to `i_out.info()`, `i_out.error()`, etc.
 
  * register the command for auto complete using `shell.add_cmd(cmd|vector<cmd>)` in `nvStore.cpp::run()` 
  
  * if adding a store manage command, one should add option information (e.g., help info) in `nvStore.cpp::init_command_parser()`

- add a store query command (e.g., `add_vertex`)

  * declare the class for the command in `query_engine.h`, making sure it is derived from the `query_base` class:
  ```cpp
  class query_add_vertex : public query_base
  {
     public:
      REGISTER_QUERY_TYPE(query_add_vertex);
      int run(struct query_param_type);
  };
  ```
  * register the command in `query_engine.cpp` and implement the `run()` method (and `option()` as well). If success, the `run()` method should return `_QUERY_SUCCESS_RET`; else return `_QUERY_FAIL_RET`
 

  ```cpp
  REGISTER_QUERY_NAME(query_add_vertex,       "add_vertex");

  int query_add_vertex::run(struct query_param_type param)
  {
    qit_type iter = param.info->find(_ID_ARG);  // get a cmd argument (defined in defines.hpp)	
    size_t vid = param.key_to_id->find(key)
    vertex_iterator_type vit = param.g->find_vertex(vid);
 
    qit_type lower, upper;
    lower = param.info->lower_bound(string("prop"));
    upper = param.info->upper_bound(string("prop"));
    if (lower != param.info->end()) {
       for (qit_type it=lower;it!=upper;it++) {
         string element = it->second;
         string pname, pvalue;
         stringParser::headParser(element, pname, pvalue);
         vit->set_subproperty(pname,pvalue);
       }
    }
    if (param.internal_output) param.internal_output->info("vertex added");
    return _QUERY_SUCCESS_RET;
  }
  
  void query_add_vertex::options(command_options & opts)
  {
      opts.add_command_info("add a new vertex");
      opts.add_option(_ID_ARG,     true,   HAS_ARGUMENT, "vertex id");
      opts.add_option(_LABEL_ARG,  false,  HAS_ARGUMENT, "vertex label", _DEFAULT_LABEL);
      opts.add_option(_PROP_ARG,   false,  MULTIPLE_ARGUMENT, "vertex property (prop_name:prop_value)");
  }


  int query_add_vertex::run(struct query_param_type param)
  {
    string key, label;

    // get key & label                                                                                                                                                                                          param.opts->get_value(_ID_ARG, key);
    param.opts->get_value(_LABEL_ARG, label);

    // insert vertex                                                                                                                                                                                            vertexd_type vid;
    if (param.key_to_id->find(key) == param.key_to_id->end())
    {
        vid = param.g->add_vertex(label);  // add vertex                                                                                                                                                     
        (*(param.key_to_id))[key] = vid;
        (*(param.id_to_key))[vid] = key;
    }
    else
    {
        vid = (*(param.key_to_id))[key];
    }

    vertex_iterator_type vit = param.g->find_vertex(vid);

    // add sub properties                                                                                                                                                                                       vit->set_subproperty(_ID_ARG_INTERNAL, key);

    string full_prop;

    // get property by calling get_value. the property is returned in full_prop                                                                                                                                 // since property is MULTIPLE_ARGUMENT, it will return a long string with                                                                                                                                   // multiple properties. for example: "prop1:pvalue1 prop2:pvalue2"                                                                                                                                          if (param.opts->get_value(_PROP_ARG, full_prop)==command_options::_get_option_arg)
    {
        string element;
        string pname, pvalue;
        size_t next=0;
        while (next != string::npos)
        {
           next = stringParser::csv_nextCell(full_prop, " ", pname, next);
 	   if (next == string::npos) break;
            next = stringParser::csv_nextCell(full_prop, " ", pvalue, next);
            //stringParser::headParser(element, pname, pvalue);                                                                                                                                                         if (pname.empty() || pvalue.empty()) break;
            vit->set_subproperty(pname,pvalue);
        }
    }

    if (param.internal_output) param.internal_output->info("vertex added");
    return _QUERY_SUCCESS_RET;
  } 		  
  ````

int query_add_vertex::run(struct query_param_type param)
{

  
  * If we need to output vertices to the output buffer:

  ```cpp
    if (param.internal_output) {
      param.internal_output->output_seg_begin("vertex",header);
      param.internal_output->output_seg_data(data);
      param.internal_output->output_seg_end();
  ````

