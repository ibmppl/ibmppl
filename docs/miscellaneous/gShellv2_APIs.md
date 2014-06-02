### Instructions on using Native Graph Store gShell version 2

gShell is a shell-like environment implemented using IBMPPL for demonstrating
how the System G native graph store works. gShell allows users to operate
multiple graph stores and it supports graphs of different edge types
(directed, undirected, pred_directed). Each command in gShell is implemented
by a function that can be easily plugged in to the system, so users can
implement additional data store operations or analytic tools in the shell. The
shell can work in interactive mode (similar to Linux terminal), server/client
mode, or batch mode.

<b> 1. Compile </b>

The compilation of gShell requires the compilation of IBMPPL runtime and System G kvstore. The compile can be done using make all in the respective directories. Here is the example.

```bash
      cd ibmppl/runtime
	  make clean; make all
      cd ibmppl/kvstore
	  make clean; make all
      cd ibmppl/apps/gShell
      make clean; make all
```

<b> 2. Usage </b>

There are 4 modes for using gShell: interactive mode, server/client mode, argument mode, and batch mode. gShel is invoked as follows:

```bash
    ./nvStore <interactive [< batch_file] |server [socket_port]|execute [arguments]> 
	./nvStoreClient <server_ip> <command+arguments> [socket_port]
```
<interactive>: start gShell in interactive mode, where a prompt will appear to ask for input commands
Batch mode is a variant of the interactive mode, where the commands stored in a text file is redirected to the interactive mode.
<execute>: start gShell in argument mode, where the command and parameters in [arguments] will be performed 
<server>: start gShell in server/client mode, communicated by IPC socket. When batch mode is invoked, user must run nvStoreClient.

Example: 

```bash
          ./nvStore service &
		  ./nvStoreClient 127.0.0.1 "<command>" 

          ./nvStore interactive
          ./nvStore interactive < script.txt
		  
          ./nvStore execute "<command>"
```

The above command starts the shell. In the shell, it asks user to input instructions to create/access any store, after the prompt sign ">>". User can create a store to for saving a particular graph type; add a vertex or an edge with properties; update the property of existing vertices/edges; perform some queries, etc.
	
<b> 3. Commands </b>	
The commonly used commands in gShell include:

- Create a store. Assuming we want to create a graph store called "<store_name>", and we want use it to store an undirected graph. Note that a graph is not necessarily to be connected in gShell; that is, a graph store can maintain a set of small graphs, but all of them must be of the same type (directed, undirected, or pred_directed). The command for creating such a store is:

```bash
         create --graph <store_name> --type <undirected|directed>
```

- To close a store, we use "close". It remove the store from memory, so that we have more memory to process other stores. Or, we can issue "close_all" to close all opened stores. So, the memory is release. It is suggested to issue such commands time by time to make the memory free. 

```bash
         close --graph <store_name>
         close_all
```
 
- List all stores and their types. This command will list all existing stores (opened or not opened) and their respective graph type (directed, undirected, pred_directed). Note that this command will not load any store if they are not opened already. 

```bash
         list_all 
```

- Find help information for all commands.

  ```bash
  <command> --help
  ````
  
- Cache the output for being used as input of later-on commands

  ```bash
  <command> [command's arguments] --out myresult
  ````
  
- Use the previous cached results as the input

  ```bash
  <command> [command's arguemnt] --in myresult
  ````

------------

- Vertices filter finds a set of vertices satisfying the conditions given
  by users. The conditions involve vertex labels and properties
  
  ```bash
  filter_vertices [--label <mylabel1> [mylabel2 ...]]
  [--prop <pname1 <operator>:<cvalue1>[,cvalue1_2]>
  [pname2:<operator>:<cvalue1>:[,cvalue2_2]] [pname3...]] 
  ````

- Edge filter finds a set of edges that satisfying the conditions given by
  users. The conditions involve edge labels and properties

  ```bash
  filter_edges [--label <mylabel1> [mylabel2 ...]]
  [--prop <pname1 <operator>:<cvalue1>[,cvalue1_2]>
  [pname2:<operator>:<cvalue1>:[,cvalue2_2]] [pname3...]] 
  ````
