### Instructions on using Native Graph Store

gShell is a shell-like environment implemented using IBMPPL for demonstrating how the System G native graph store works. gShell allows users to operate multiple graph stores and it supports graphs of different edge types (directed, undirected, pred_directed). Each command in gShell is implemented by a function that can be easily plugged in to the system, so users can implement additional data store operations or analytic tools in the shell. The shell can work in interactive mode (similar to Linux terminal), server/client mode, or batch mode.

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
    ./nvStore <interactive|server|execute> [arguments] [< batch_file]
	./nvStoreClient <server_ip> <command+arguments>
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
         create <store_name> <undirected|directed|pred_directed>
```

- Now, we have <store_name> as an empty graph. A easy way to populate the store is to convert a file, say .csv files or edge list, to the edge store. In the following example, we assume that we have a edge list in csv format called <csv_file>, where each line in the fileconsists of <source node> <target node> <edge weight>. User must indicate that the source and target nodes are given by the <colID_src> and <colID_targ> columns, respectively. The data in the rest columns are treated as the properties on this edge. Note that this command must follow a store name, since gShell can concurrently operate multiple graph stores. If the first row of the .csv file is the header, then users must specify "has_header". We can use comma, tab or blank space to separate columns in the .csv file. The separator is specified by [separators]. If a string contains these separator characters. 

```bash
         <store_name> load_csv_edges <csv_file> <colID_src> <colID_targ> [has_header|no_header] [separators]
```         

- Note that in the above edge list file (or .csv file)  we can only have edge properties. In order to create a graph with both edge and vertex properties, we need and additional .csv file. We can run the above operation first to build the graph with edge properties. Then we can read a vertex file to load vertex properties. In the following example, the <colID_vtx>-th column in the vertex file gives the ID of a vertex and the rest columns give the properties of the vertex as a vector of strings. 

```bash
         <store_name> load_csv_vertices <csv_file> <colID_vtx> [has_header|no_header]  [separators]
```

- It is possible to run some analytic routines using the data store. Any graph analytic applications that are developed using System G middleware APIs shall be easily plugged into the shell. In this command, we use a collaborative filter code. The application queries a vertex called <vertex_id> in the graph store and performs BFS for <#hops> levels. It computes the number of paths from the root vertex to any leaves and rank these leaves accordingly in descending order. The top <#ranks> vertices are returned. The result can be formatted into json format if the optional argument [json] is specified.

```bash
         <store_name> colFilter  <vertex_id>  <#hops>  <#ranks> [json]
```		  

- There is a relevant command called centroid visualization for recommandation (centroid_visual). The first argument <vertex_id> for this command is also the queried vertex ID, but it performs a 2 hops colFilter and got the top <#rank1> nodes, and then for each of them perform 2 hops again and get the top 10 nodes. The results are of the top #rank from the 1st colFilter and the top <#rank2> of the remaining colFilter are aggregated to return. The result can be formatted into json if the optional argument is specified.

```bash
         <store_name>  centroid_visual <vertex_id> <#rank1> <#rank2> [jason]
```

- gShell supports interactive graph updates. Here are some examples to add/update vertices/edges. The instruction line also starts with the store name to identify which store to work on, which is followed by the command. The first argument for add_vertex is the vertex ID, and the rest are the vertex properties as a vector of strings. We actually store the vertex ID as the first property. We can update the properties using update_vertex and/or update_edge. In the following example, then "John" is the ID of the vertex and the rest are all properties, separated by blank spaces. Quotes string can include spaces or other characters. If edge (2nd example), the next two words are the source and target vertices and the rest are properties. The number of properties for vertices and edges are arbitrary (0 to 2^64).

```bash
         <store_name> add_vertex/update_vertex <vertex_id> [property list]
		 <store_name> add_edge/update_edge <src_vid> <targ_vid> [property list]
```

Here are some examples:

```bash
           mystore add_vertex    John       "These are my desk, table, and chair"  1000.00
           mystore add_edge      Mary John  "They are friends" 2011-11-11 "good friend" active
           mystore update_vertex John       "These are my books and laptop" 
           mystore update_edge   Mary John  "They are close friends" 2011-12-12 active NYC
```

- The query of a vertex or edge gives all the properties (including the adjacent edges for a vertex). We use the source vertex ID plus the target vertex ID to identify an edge. In the following example, we query the properties, adjacent edges of vertex John and then query the properties of edge (Mary, John).

```bash
         <store_name> query_vertex  <vertex_id>
         <store_name> query_edge    <src_vtx> <targ_vtx>
```

- The deletion is straightforward. We just delete the vertex or edge by giving the ID or the source and target IDs. 

```bash
         <store_name> delete_vertex <vertx_id>
         <store_name> delete_edge <src_vtx> <targ_vtx>
```		   

- The print_all command prints all contents of a graph store and show the structural information including internal IDs. It is not recommended to use this command for large graphs.

```bash
         <store_name> print_all
```

- To query all neighbors of a vertex, we use the following command. We just need to provide a vertex ID. 

```bash
         <store_name> query_neighbors <vertex_id>  
```

- To close a store, we use "<store_name> close". It remove the store from memory, so that we have more memory to process other stores. Or, we can issue "close_all" to close all opened stores. So, the memory is release. It is suggested to issue such commands time by time to make the memory free. 

```bash
         <store_name> close
         close_all
```
 
- We have a plug-in analytic call pageRank, which performs persistent page rank in a pred_directed graph. By persistent page rank, we mean that the importance of each vertex is stored in each iteration. Thus, we can incrementally perform page rank at any time, or after any changes to the graph. The arguments for the command are the damping factor, the quadratic error bound and the initialization control. The damping factor and quadratic error are explained in wiki. By specifying "restart", we re-initialize the importance of each vertex; otherwise, if we omit it, we use the current stored values for ranking. Note that due to a lot of string to number conversions, the performance might be adversely impact. For performing high-performance page rank, please choose our in-memory page ranking subroutine in "apps/pagerank/" directory.

```bash
         <store_name> pageRank <damping_factor> <quadratic_error> [restart]
```

- List all stores and their types. This command will list all existing stores (opened or not opened) and their respective graph type (directed, undirected, pred_directed). Note that this command will not load any store if they are not opened already. 

```bash
         list_all 
```

- Erase a store from the disk. This is a permanent deletion and can not be recovered. So, this command should be used in cautious. 

```bash
        delete <store_name>
```
More commands and plugin analytics are addition to gShell. Please contact Yinglong Xia for further information.



