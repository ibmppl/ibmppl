### Instructions on using Native Graph Store

gShell is a shell-like environment implemented using IBMPPL for demonstrating how the System G native graph store works. gShell allows users to operate multiple graph stores and it supports graphs of different edge types (directed, undirected, pred_directed). Each command in gShell is implemented by a function that can be easily plugged in to the system, so users can implement additional data store operations or analytic tools in the shell. The shell can work in interactive mode (similar to Linux terminal), server/client mode, or batch mode.

<b> 1. Compile </b>

The compilation of gShell requires the compilation of IBMPPL runtime and System G kvstore. The compile can be done using make all in the respective directories. Here is the example.

```bash
      cd ibmppl/runtime
	  make clean all
      cd ibmppl/kvstore
	  make clean all
      cd ibmppl/apps/gShell_v2
      make clean all
```

<b> 2. Usage </b>

There are 5 modes for using gShell: interactive mode, server/client mode,
argument mode, batch mode, and multiuser mode. The following discussion
assumes the use of interactive mode, although it applies to other modes as
well. gShell can be invoked as follows:

```bash
    ./nvStore <interactive [< batch_file] |server [socket_port]|execute [arguments] | multiuser> 
	./nvStoreClient <server_ip> <command+arguments> [socket_port]
```
<interactive>: start gShell in interactive mode, where a prompt will appear to ask for input commands
Batch mode is a variant of the interactive mode, where the commands stored in a text file is redirected to the interactive mode.
<execute>: start gShell in argument mode, where the command and parameters in [arguments] will be performed 
<server>: start gShell in server/client mode, communicated by IPC socket. When
    batch mode is invoked, user must run nvStoreClient.
<multiuser>: start gShell by gShellSuperMgr, another code in the folder, so that multiple gShell instances
    can work concurrently, coordinated by the supermanager. This is for
    providing gShell as service on Cloud.

Example: 

```bash
          ./nvStore service &
		  ./nvStoreClient 127.0.0.1 "<command>" 

          ./nvStore interactive
          ./nvStore interactive < script.txt
		  
          ./nvStore execute "<command>"
```

For personal use, the interactive mode is recommand, as it comes with a simple
shell environment along with help info (by clicking the tab key). 

The above command starts the gShell. In the shell, it asks user to input
instructions to create/access any store, after the prompt sign ">>". User can
create a store to for saving a particular graph type; add a vertex or an edge
with properties; update the property of existing vertices/edges; perform some
queries, etc.

In the interactive mode, the help info can be obtained by click the tab key:
```bash
bash-4.1$ ./nvStore interactive
directory is created: database/
gShell>>
add_edge                           add_vertex
analytic_betweenness_centrality    analytic_bfs
analytic_closeness_centrality      analytic_clustering_coefficient
analytic_colfilter                 analytic_connected_component
analytic_degree_centrality         analytic_egonet
analytic_k_core                    analytic_k_shortest_paths
analytic_reset_engine              analytic_shortest_paths
analytic_start_engine              analytic_stop_engine
analytic_triangle_count            delete_eprop
delete_vprop                       export_csv
filter_edges                       filter_vertices
find_edge                          find_multiple_vertex
find_neighbors                     find_random_edges
find_random_vertices               find_vertex
find_vertex_max_degree             get_num_edges
get_num_vertices                   get_vertex_degree
load_csv_edges                     load_csv_vertices
print_all                          set_max_mem
span_graph                         update_edge
update_vertex                      visual_loading
close                              close_all                          
open                               delete
create                             list_all
help                               version
```
where all the available commands are listed on the screen. When you are in the
middle of inputing a command, you can press `tab` once for auto-completing the
input. If the input is not unique given what you have typed in, you can
pressed `tab` twice, it will list all choices. Similarly, by pressing `tab`,
it can auto-complete the arguments and file paths.

By typing in the command `help`, it shows some useful hint on using the shell: 
```bash
gShell>> help
[help]
{
"info":[
{"MESSAGE":"<tab>:      list all available commands"},
{"MESSAGE":"ab<tab>:    auto complete the command all list all commands starting with ab"},
{"MESSAGE":"Ctrl+C:     quick exit"},
{"MESSAGE":"up/down:    find the previous/nest command"},
{"MESSAGE":"left/right: move cursor for editing a command"},
{"MESSAGE":"additional help and tutorials avaiable at https://github.com/ibmppl/ibmppl"}
]
}
```

Each command in gShell comes with an argument `--help` for displaying the
argument info. This is helpful if we do not want to memorize all argument
information. Argument without mark `[optional]` is a must.

By default, the output information is always organized as in JSON format, although
you can convert it into a more human readable format by specifying `--format
plain` in each command. 

```bash
gShell>> list_all
[list_all]
{
"warning":[{"MESSAGE":"store is empty!"}]
}
gShell>> list_all --help
[list_all] [--help]
{
"info":[
{"MESSAGE":"list_all - list all graphs"},
{"MESSAGE":"--format:  [optional] output format"},
{"MESSAGE":"--help:  [optional] help infomation"}
]
}
gShell>> list_all --help --format plain
[list_all] [--help] [--format] [plain]
---------------------------------------
STORE NAME      COMMAND
[]      list_all
---------------------------------------
<info>
        MESSAGE
		list_all - list all graphs
<info>
	    MESSAGE
		--format:  [optional] output format
<info>
		MESSAGE
		--help:  [optional] help infomation
---------------------------------------
```
	
<b> 3. Commands </b>	
The commonly used commands in gShell include the follows. Please use `tab tab`
to see the complete command lists. Besides, this tutorial discusses ususally
used parameters for each command, not the complete parameter lists. For the
full list, again please use `<command> --help` for details. All the commands
are built on `ibm_generic_graph.hpp` class, so you can also view this gShell
as an advanced example for using the System G Native Store programming APIs.  

- Create a store. Assuming we want to create a graph store called
  "<graph_name>", and we want use it to store an undirected graph. Note that a
  graph is not necessarily to be connected in gShell; that is, a graph store
  can maintain a set of small graphs, but all of them must be of the same type
  (directed, or undirected). The command for creating such a graph store is:

```bash
         create --graph <graph_name> --type <undirected|directed>
```

- To close a store, we use "close". It removes the store from memory, so that
  we have more memory to process other graphs. Or, we can issue "close_all" to
  close all opened graphs. So, the memory is released. It is suggested to
  issue such commands time by time to make the memory free. Note that gShell
  can capture `Ctrl+c` and interpret it as a `close_all` command. 

```bash
         close --graph <graph_name> 
         close_all
```
 
- List all stores and their types. This command will list all existing stores (opened or not opened) and their respective graph type (directed, undirected, pred_directed). Note that this command will not load any store if they are not opened already. 

```bash
         list_all 
```

- Erase a store from the disk. This is a permanent deletion and can not be recovered. So, this command should be used in cautious. 

```bash
        delete --graph <graph_name>
```

- Now, we have <graph_name> as an empty graph. A easy way to populate the
  store is to convert a file, say .csv files or edge list, to the edge
  store. In the following example, we assume that we have a edge list in csv
  format called <csv_file>, where each line in the fileconsists of <source
  node> <target node> <edge weight>. User must indicate that the source and
  target nodes are given by the <colID_src> and <colID_targ> columns,
  respectively. The data in the rest columns are treated as the properties on
  this edge. Note that this command must follow a store name, since gShell can
  concurrently operate multiple graph stores. If the first row of the .csv
  file is the header, then users must specify "has_header". We can use comma,
  tab or blank space to separate columns in the .csv file. The separator is
  specified by [separator], such as "," or ":". If a string contains these
  separator characters, each char should work. 

```bash
         load_csv_edges --graph <graph_name> --csvfile <csv_file> --srcpos
         <colID_src> --targpos <colID_targ> [--no_header] --separator <,>
```         

- Note that in the above edge list file (or .csv file)  we can only have edge properties. In order to create a graph with both edge and vertex properties, we need and additional .csv file. We can run the above operation first to build the graph with edge properties. Then we can read a vertex file to load vertex properties. In the following example, the <colID_vtx>-th column in the vertex file gives the ID of a vertex and the rest columns give the properties of the vertex as a vector of strings. 

```bash
         load_csv_vertices --graph <graph_name> --csvfile <csv_file> --keypos
         <colID_vtx> [--no_header]  --separator <,>
```

- gShell supports interactive graph updates. Here are some examples to add/update vertices/edges. The instruction line also starts with the store name to identify which store to work on, which is followed by the command. The first argument for add_vertex is the vertex ID, and the rest are the vertex properties as a vector of strings. We actually store the vertex ID as the first property. We can update the properties using update_vertex and/or update_edge. In the following example, then "John" is the ID of the vertex and the rest are all properties, separated by blank spaces. Quotes string can include spaces or other characters. If edge (2nd example), the next two words are the source and target vertices and the rest are properties. The number of properties for vertices and edges are arbitrary (0 to 2^64).

```bash
         add_vertex/update_vertex --graph <graph_name> --id <vertex_id> --prop
         name1:value1 name2:value2 ...
		 add_edge/update_edge --graph <graph_name> --src <src_vid> --targ
         <targ_vid> --prop name1:value1 name2:value2 ...
```

Here are some examples:

```bash
         add_vertex  --graph g  --id "John"   --prop memo:"These are my desk, table, and chair"  income:"1000.00"
         add_edge    --graph g  --src "Mary" --targ John  --prop memo:"They are friends" time:"2011-11-11"
         update_vertex --graph g --id "John"    --prop memo:"These are my books and laptop" 
         update_edge  --graph g  --src "Mary" --targ "John"  --prop memo:"They are close friends" time:"2011-12-12"
```

- The query of a vertex or edge gives all the properties (including the adjacent edges for a vertex). We use the source vertex ID plus the target vertex ID to identify an edge. In the following example, we query the properties, adjacent edges of vertex John and then query the properties of edge (Mary, John).

```bash
         find_vertex --graph <graph_name>  --id <vertex_id>
         find_edge  --graph <graph_name>  --src <src_vtx> --targ <targ_vtx>
```

- The deletion is straightforward. We just delete the vertex or edge by giving the ID or the source and target IDs. 

```bash
         delete_vertex --graph <graph_name> --id <vertex_id>
         delete_edge --graph <graph_name> --src <src_vtx> --targ <targ_vtx>
```		   

- The print_all command prints all contents of a graph store and show the structural information including internal IDs. It is not recommended to use this command for large graphs.

```bash
         print_all --graph <graph_name>
```

- To get the number of edges and vetices in a graph, we use the following commands.

```bash
         get_num_vertices --graph <graph_name>
	 get_num_edges --graph <graph_name>
```
- To get the number of neighbors of a vertex

```bash
         get_num_neighbors --graph <graph_name> --id <vertex_id>
```

- To query all neighbors of a vertex, we use the following command. We just need to provide a vertex ID. 

```bash
         find_neighbors --graph <graph_name> --id <vertex_id>  
```

- Filter vertices to only output those with the i-th property equal to val

```bash
         filter_vertices --graph <graph_name> --condition <expression_with_propName>
```

- Find the vertex with the maximum node degree. If the condition i and val are given, it finds the vertex only from those satisfying the condition, i.e., the i-th property of the vertex is equal to val. It also finds the vertices with the top #n number of degrees. 

```bash
        find_vertex_max_degree --graph <graph_name> --edgetype <in|out|all>
```

- Find n vertices randomly from a graph. This command is for users to get some vertices, so that they can use such vertices as start points for certain analytics. <n> is a number, say 10.

```bash
        find_random_vertices --graph <graph_name> --num <n>
```
- Find n edgess (nearly) randomly from a graph. This command is for users to get some edges, so that they can use such vertices as start points for certain analytics. <n> is a number, say 10.

```bash
        find_random_edges --graph <graph_name> --num <n>
```
<!--
- For each vertex with the i-th property equal to val_1, find all its neighbors. Then, for each neighbor v, find all v's neighbor set U, where each one has its j-th property equal to val_2. For each u in U, find the total number of visits and output the one with the maximum visits. A more specific example could be: Given a graph consisting of nodes of device types, IPs, and URLs, grouped by device type, find the most popular URL (i.e., the URL vertex with the most neighbors of IP) for each group. 

```bash
        <graph_name> find_vertex_max_degree_by_group <i> <val_1> <j> <val_2>
```

- To query the property keys of the vertices and edges, we use the following commands. If there is no such keys (i.e., the data was imported with arguemnt "no_header"), a notice is shown to tell that there is no property keys.

```bash
        <graph_name> query_vpropkeys
		<store_name> query_epropkeys
```
-->

<b> 4. Plug-In Analytics </b>

- A user controled Breadth First Search (BFS) can be invoked by the following commands. <root> is an arbitrary vertex in the graph stored in <graph_name>, and #hops shows the maximum allowed BFS levels. <max_breadth_per_level> gives the maximum number of vertices to traverse at each BFS level. This is for visualization purpose, where we do not want to visualize all the edges for dense vertices. 

```bash
         analytic_bfs --graph <graph_name> --id <root> --depth <#hops> --width <max_breadth_per_level>
```

- It is possible to run some analytic routines using the data store. Any graph analytic applications that are developed using System G middleware APIs shall be easily plugged into the shell. In this command, we use a collaborative filter code. Collaborative filter is widely used in recommandation systems and has many alternatives. In this version, it takes a bipartite graph G((X, Y), E) as the input, and finds <i>relevant</i> vertices to a user specificed vertex, say x∈X. The most relevant vertex is z = argmax |neighbors(x) ^ neighbors(z)| for any z∈X.  The analytics queries a vertex called <vertex_id> in the graph store and performs BFS for <#hops> levels. It computes the number of paths from the root vertex to any leaves and rank these leaves accordingly in descending order. The top <#ranks> vertices are returned. 

```bash
         analytic_colfilter --graph <graph_name> --id <vertex_id> --depth <#hops> --topnum <#ranks>
```		  

- We have a plug-in analytic call pageRank, which performs persistent page rank in a pred_directed graph. By persistent page rank, we mean that the importance of each vertex is stored in each iteration. Thus, we can incrementally perform page rank at any time, or after any changes to the graph. Given a directed graph G(V, E), pageRank works by counting the number and quality of edges to a vertex to determine a rough estimate of how important the vertex is in the graph. The quality is iteratively computed by: PR(v_i) = (1-d)/N + d ∑<sub>{v_j∈ neighbors(v_i)}</sub> PR(v_j)/L(v_j), where N=|V|; d is the damping factor and L(v_j) is the number of outgoing edges of vertex v_j. The underlying assumption is that more important websites are likely to receive more links from other websites. The arguments for the command are the damping factor, the quadratic error bound and the initialization control. The damping factor and quadratic error are explained in wiki. By specifying "restart", we re-initialize the importance of each vertex; otherwise, if we omit it, we use the current stored values for ranking. Note that due to a lot of string to number conversions, the performance might be adversely impact. For performing high-performance page rank, please choose our in-memory page ranking subroutine in "apps/pagerank/" directory.

```bash
         analytic_pagerank --graph <graph_name> --damp <damping_factor> --quad <quadratic_error> --restart
```

- ConnectedComponent, which finds all connected components in a graph. It takes an undirected graph as input and outputs in json format the following information: 1) a list of all the nodes in the graph with the component label for each node, 2) a list of all the edges in the graph with the component label for each edge, 3) a list of connected component with the labels of nodes contained in each component. To run:

```bash
         analytic_connected_component --graph <graph_name>
```

- kCore, which finds the K-core of a graph, where K is a parameter specified by the user. A K-core of a graph G is a maximal connected subgraph of G in which all nodes have degree at least K. It takes an undirected graph and K as input and outputs in json format the following information: 1) a list of nodes in the K-core, 2) a list of edges in the K-core. To run:

```bash
         analytic_k_core --graph <graph_name> --k <k>
```

- ClusteringCoefficient, which computes the local clustering coefficient of each node in an undirected or directed graph. Let N be the neighborhood of a node (immediately connected neighbors), let n be |N|, i.e. size of N. The local clustering coefficient C of this node is the number of links (edges) between the nodes within N divided by n*(n-1) for a directed graph or n*(n-1)/2 for an undirected graph. It takes a graph (undirected or directed) as input and outputs in json format the following information: 1) a list of all the nodes in the graph with the local clustering coefficient value for each node, 2) a list of all the edges in the graph. To run:

```bash
         analytic_clustering_coefficient --graph <graph_name> 
```

- TriangleCount, which computes the triangle count on each node of an undirected or directed graph. For a directed graph, it counts the total number of in-, out-, through-, and cycle-triangles separately. It takes a graph (undirected or directed) as input and outputs in json format the following information: 1) a list of triangles with type and count information, 2) a list of all the nodes in the graph with the triangle count(s) for each node, 3) a list of edges that belong to the triangles. To run:

```bash
         analytic_triangle_count --graph <graph_name> 
```

- ShortestPaths, which computes the shortest paths from a given node to any other node in an undirected or directed graph, and two closeness centrality measures: 1) using the original formula, which is C(i)=1/(sum(shortest_distance(i, j)) for all j != i, 2) using Opsahl 2010 formula, which is C(i) = sum(1/shortest_distance(i, j)) for all j != i. It takes a graph (undirected or directed, with optional weight on each edge specified in the edge list data file) and the label of the target node as input and outputs in json format the following information: 1) a list of nodes with shortest distance value, number of shortest paths, and shortest paths (number of hops, sequence of nodes on each path) information from the target node to each of these nodes, 2) the closeness centrality measures of the target node, 3) a list of all the edges in the graph. To run:

```bash
         analytic_shortest_paths --graph <graph_name> --hidepath --ignoredgeweight --sinkvertex <source_node> --sinkvertex <target_node>
```


<b> Note </b>

More commands and plugin analytics are addition to gShell. Please contact Yinglong Xia for further information.



