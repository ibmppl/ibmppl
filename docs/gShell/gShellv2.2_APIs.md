## Instructions on using Native Graph Store gShell (v2.2) ##



gShell is a shell-like environment implemented using IBMPPL for demonstrating
how the IBM System G native graph store works. gShell allows users to operate
multiple graph stores and it supports graphs of different edge types
(e.g. directed, undirected). Each command in gShell is implemented by a
function that can be easily plugged in to the system, so users can implement
additional graph store operations or analytic tools in gShell. gShell can work
in a number of modes (described in detail in Section 2 Usage) such as
interactive mode (similar to Linux terminal), batch mode, server/client mode,
and multiuser mode.



<b> 1. Compile </b>



The compilation of gShell requires the compilation of IBMPPL tools, runtime
and IBM System G kvstore, which can be done using `make all` in the respective
directories, as shown below:



```bash

cd ibmppl/tools

make clean all

cd ibmppl/runtime

make clean all

cd ibmppl/kvstore

make clean all

cd ibmppl/apps/gShell_v2.2

scl enable devtoolset-1.1 bash

make clean all

```



<b> 2. Start </b>



In this document, <...> is used to indicate the value of an argument,
e.g. <graph_name> indicates the argument for the name of the graph. gShell can
be invoked in any of the following modes:



Interactive mode:

```bash
    ./gShell interactive
````


gShell displays a prompt “>>” waiting for input commands. To exit, type
`close_all` or `Ctrl-c`.



Batch mode:

./gShell interactive < <batch_file> (e.g., ./gShell interactive < script.txt)



The batch mode is a variant of the interactive mode, where the commands stored
in a text file <batch_file> are redirected to the interactive mode (using “<”)
and executed sequentially. Note that `close all` needs to be included as the
last command in the file in order exit from gShell.



Server/client mode:

```bash
./gShell server <socket_port> (e.g., ./gShell server 9998)

./gShellClient <server_ip> “<command+arguments>” <socket_port> (e.g.,
./gShellClient 127.0.0.1 "create --graph g --type undirected" 9998)
```


The communication between server and client is through IPC socket.



Multi-user server/client mode:

```bash
./gShellSuperMgr 7755

./gShellClientMulti “<command+arguments>” <username> <server_ip> <socket_port>
(e.g., ./gShellClientMulti “create --graph g --type undirected”
user123 127.0.0.1 7755
```


The multi-user mode allows multiple gShell instances to work concurrently, one
gShell instance per user. gShellSuperMgr manages all gShell instances and
coordinates client communications from multiple users. If the port number is
not specified for gShellSuperMgr, the default port number of 7755 is used.



<b> 3. Commands </b>

In the interactive mode, pressing the `tab` key results in a list of all the
available commands to be displayed. Each command in gShell comes with an
argument `--help` for displaying the argument information. Arguments can be
specified in any order. Those not marked as `[optional]` are
mandatory. Argument values containing space must be quoted.



Commands in gShell can be categorized into two groups: shell operation
commands (including `help`, `list_all`, `close_all`, `version`), and store
operation commands. Store operation commands perform against a particular
graph store. Since gShell can concurrently operate multiple graph stores, a
store name must be provided for the `--graph` argument for these commands.



When in the middle of inputting a command, we can press `tab` once for
auto-completing the

input. If the input is not unique given what we have typed in, we can press
`tab` twice to list all choices. Similarly, we can request auto-completion of
the arguments and file paths by pressing `tab`.



Typing in the command `help` shows some useful hints on using gShell:



```bash
gShell>> help

[help]

{
"info":[
{"MESSAGE":"<tab>: list all available commands"},
{"MESSAGE":"ab<tab>: auto complete the command or list all commands starting with ab"},
{"MESSAGE":"Ctrl+C: quick exit"},
{"MESSAGE":"up/down: find the previous/nest command"},
{"MESSAGE":"left/right: move cursor for editing a command"},
{"MESSAGE":"additional help and tutorials available at https://github.com/ibmppl/ibmppl "}
]
}

```



By default, the output information is always organized in JSON format, but we
can request a more human readable format by specifying `--format plain` in
each command.



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
{"MESSAGE":"--format: [optional] output format"},
{"MESSAGE":"--help: [optional] help infomation"}
]

}

gShell>> list_all --help --format plain

[list_all] [--help] [--format] [plain]

---------------------------------------

STORE NAME COMMAND

[] list_all

---------------------------------------

<info>

MESSAGE

 list_all - list all graphs

<info>

 MESSAGE

 --format: [optional] output format

<info>

 MESSAGE

 --help: [optional] help infomation

---------------------------------------

```



Other common arguments include `--redirect <file_path>` to redirect shell
output to a file on disk, `--out <cache_name>` to cache the result of a
command (in the format of vertex and edge IDs), `--in <cache_name>` to use the
cached result of a previous command as input, essentially chaining together
multiple commands (i.e., the output of the first command becomes the input of
the second command and so on).



Below we describe the commonly used commands in gShell. Note that this
documentation discusses commonly used arguments for each command, not
necessarily the complete argument list. For the complete argument list of each
command, please use the ` --help` argument. Any argument in [...] is
optional. Argument values in {...} are predetermined. (...|...) indicates that
one of the enclosed arguments needs to be specified.



- Create a store: `create`
```bash
create --graph <graph_name> [--type <{undirected, directed}>]
```
> If `--type` is not specified, a directed graph is created by default. Note
that the graph in a graph store is not necessarily connected; that is, a graph
store can maintain a set of small graphs, but all of them must be of the same
type (directed, or undirected).



- Populate a store: `load_csv_edges`, `load_csv_vertices`

```bash
load_csv_edges --graph <graph_name> --csvfile <edge_csv_file> --srcpos
<col#_src> --targpos <col#_targ> [--labelpos <col#_ label>]
[--label <edge_label>] [--no_header] [--separator <,>]

load_csv_vertices --graph <graph_name> --csvfile <vertex_csv_file> --keypos
<col#_vid> [--labelpos <col#_label>] [--label <vertex_label>] [--no_header]
[--separator <,>]
```



After the `create` command is executed, we have <graph_name> as an empty graph
store. An easy way to populate the store is to import vertex and edge
information from files. Each line in the edge csv file provides information
about one edge. `--srcpos` and `--targpos` indicate the respective positions
of the columns in the edge csv file that correspond to the source and target
vertex IDs of each edge (the position of the first column is 0). The data in
the rest of the columns are treated as the properties on each edge. The label
of an edge is considered a special property. `--labelpos` is used to indicate
the column position of the label value (optional). Alternatively, we can use
`--label` to provide a label to be applied to all the vertices or edges in the
file. If the csv file has no header, then we must specify
`--no_header`. gShell automatically recognizes the use of comma, tab or space
to separate columns in the csv file. The separator (e.g. "," or ";") is
specified with `--separator` (optional). If the string value of this argument
contains multiple characters, each character is treated as a separator.



Note that in the edge csv file we can only have edge properties. Vertex csv
files are used to specify vertex properties. `--keypos` is used to specify the
column number (starting from 0) in the vertex csv file that corresponds to the
ID of each vertex, `--labelpos` provides the column number for the label of
each vertex, and the rest of the columns specify the properties of the vertex
as a vector of strings.



Multiple vertex or edge csv files can be loaded to a single graph store, which
allows vertex or edge with different types and properties to be
supported. Note that multiple occurrences of the same source and target pair
are treated as multiple edges.



- Update a store: `add_vertex`, `add_edge`, `update_vertex`, `update_edge`,
  `delete_vprop`, `delete_eprop`

```bash

add_vertex --graph <graph_name> --id <vertex_id>
[--prop <name1:value1 name2:value2 ...>] [--label <label_name>]

add_edge --graph <graph_name> --src <src_vid> --targ <targ_vid>
[--prop <name1:value1 name2:value2 ...>] [--label <label_name>]

update_vertex --graph <graph_name> --id <vertex_id> --prop <name1:value1
name2:value2 ...>

update_edge --graph <graph_name> --src <src_vid> --targ <targ_vid> --prop
<name1:value1 name2:value2 ...> [--label <edge_label>] [--eid <edge_id>]

delete_vprop --graph <graph_name> --id <vertex_id> --prop <name1:value1
name2:value2 ...>

delete_eprop --graph <graph_name> --src <src_vid> --targ <targ_vid> --prop
<name1:value1 name2:value2 ...> [--label <edge_label>] [--eid <edge_id>]

```



Multiple values of `--prop` are separated by space. Property name or value
containing space must be quoted. The number of properties for vertices and
edges is arbitrary (0 to 2^64). If there are multiple edges between a pair of
vertices, use `--eid` to specify a particular edge. `--label` filters to
edge(s) of a specific label. Otherwise, all the edges are affected.



Note that currently update to vertex or edge label is not supported. In
additional, “label”, “exid”, and “vclass” (case sensitive) are reserved for
internal use and should not be used as property names.



Examples:

```bash

add_vertex --graph g --id John --prop memo:"These are my desk, table, and
chair" income:1000.00 --label person

add_edge --graph g --src Mary --targ John --prop memo:"They are friends"
time:"2011-11-11"

update_vertex --graph g --id John --prop memo:"These are my books and laptop"

update_edge --graph g --src "Mary" --targ "John" --prop memo:"They are close
friends" time:"2011-12-12"

delete_vprop --graph g --id John --memo

delete_eprop --src Mary --targ John --prop memo time

```



- Open a store: `open`

```bash

open --graph <graph_name>

```



Opening a store loads the essential information needed for graph access from
disk to memory. The rest of the graph is loaded into memory on demand
according to the requirements of each individual command. When a command is
issued against a particular graph store, the store is automatically opened if
not already. Therefore, it is not necessary to use this command explicitly.



- Save/close a store: `close`, `close_all`

```bash

close --graph <graph_name>

close_all

```



Closing a store persists it on disk and removes the store from memory, so that
we have more memory to process other graphs. Or, we can use `close_all` to
close all opened graphs in order to release memory. gShell captures `Ctrl-c`
and interpret it as the `close_all` command.



Note that the `close` command must be used if the graph store is to be
persisted on disk and loaded into memory at a later time.



- List all stores and their types: `list_all`

```bash

list_all

```



This command will list all existing stores (opened or not opened) and their
respective graph types (directed, undirected). Note that this command will not
load (open) any store if they are not opened already.



- Erase a store from the disk: `delete`

```bash

delete --graph <graph_name>

```



This is a permanent deletion and cannot be recovered. So, this command should
be used with caution.





- Print a store: `print_all`

```bash

print_all --graph <graph_name>
[--format <{json, plain, vertexcsv, edgecsv, internal}>] [--in <cache_name>]

```



This command prints all vertices and edges (with properties) of the whole
graph from a graph store, or the sub-graph stored in <cache_name>. It is not
recommended to use for large graphs.

If `--format vertexcsv` is specified, only vertex information is displayed in
csv format. Similarly, if `--format edgecsv` is specified, only edge
information is displayed in csv format.



- Export a store to external csv files: `export_csv`

```bash

export_csv --graph <graph_name> --path <directory>

```



If there are different types of vertices with different properties, gShell
creates one vertex csv file for each type of vertices. Similarly, if there are
different types of edges with different properties, gShell creates one edge
csv file for each type of edges. As a result, multiple vertex/edge csv files
may be created in the <directory>.



- Get the size of a store: `get_num_vertices`, `get_num_edges`

```bash

get_num_vertices --graph <graph_name> [--in <cache_name>]

get_num_edges --graph <graph_name> [--in <cache_name>]

```



If `--in` is used, the numbers are for the subgraph stored in <cache_name> as
the result of a previously issued command.



- Get all information about vertex or edge: `find_vertex`, `find_edge`

```bash

find_vertex --graph <graph_name> ([--id <vertex_id>] | [--in <cache_name>])
[--out <cache_name>]

find_multiple_vertex --graph <graph_name> --id <vertex_id1 vertex_id2 ...>
[--out <cache_name>]

find_edge --graph <graph_name> ([--src <src_vid>] [--targ <targ_vid>]
[--eid <edge_id>] | [--in <cache_name>]) [--label <edge_label>]
[--out <cache_name>]

```



For `find_vertex`, the input comes from either `--id` for a single vertex or
`--in` for a set of vertices. For `find_edge`, the input comes from either
`--src` and `--targ` or `--in`. `--eid` is used in combination with `--src`
and `--targ` to get a particular edge when there may be multiple edges between
them. `--label` is used to filter to edges with a particular label.



- Find the vertex with the maximum degree (number of neighbors):
  `find_vertex_max_degree`

```bash

find_vertex_max_degree --graph <graph_name> [--edgetype <{in, out, all}>]

```



If there are multiple such vertices, only one is returned.



- Get neighbor information of vertex: `get_vertex_degree`, `find_neighbors`

```bash

get_vertex_degree --graph <graph_name> --id <vertex_id>

find_neighbors --graph <graph_name> ([--id <vertex_id>] | [--in <cache_name>])
[--label <edge_label>] [--out <cache_name>]

```

For `find_neighbors`, the vertex information comes from either `--id` or
`--in`. If `--label` is specified, gShell returns only neighbors whose edges
between them and the given vertex have the specified label.



- Filter vertices or edges by label or property: `filter_vertices`,
  `filter_edges`

```bash

filter_vertices --graph <graph_name> [--label <label1 label2 ...>]
[--prop <name1 name2 ...>] [--condition “<expression>”]

filter_edges --graph <graph_name> [--label <label1 label2 ...>]
[--prop <name1 name2 ...>] [--condition “<expression>”]

```



To filter by label (separate multiple labels by space), use `--label`. To
filter by existence of certain properties, use `--prop` to specify the names
of the properties. To filter by property values, use `--prop` to specify the
names of the properties (separated by space), and use `--condition` to specify
the expression (must be quoted) for evaluating the values of the specified
properties.



Examples:

```bash

filter_vertices --graph g --label A --prop tag

filter_vertices --graph g --label A B --prop tag value --condition “tag==T ||
(value>0.3 && value < 0.9)”

filter_edges --graph g --label a --prop weight

filter_edges --graph g --label a b --prop weight --condition “weight <0.2 ||
weight > 0.7”

```



- Get random vertices or edges from a graph store: `find_random_vertices`,
  `find_random_edges`

```bash

find_random_vertices --graph <graph_name> --num <n> [--out <cache_name>]

find_random_edges --graph <graph_name> --num <n> [--out <cache_name>]

```



These commands are useful for getting a sub-graph. `--num` specifies the
number of vertices or edges returned. Note that the result may contain
duplicates. `--out` is used to save the result for later use.



- Get egonet of a vertex: `get_egonet`

```bash

get_egonet --graph <graph_name> --id <vertex_id> [--depth <num_hops>]
[--out <cache_name>]

```

If `--depth` is not specified, the default value of 1 is used.



- Get the induced subgraph given a list of vertices: `get_subgraph`

```bash

get_subgraph --graph <graph_name> ([--id <vertex_id1 vertex_id2 ...>] |
[--in <cache_name>]) [--out <cache_name>]

```



<b> 4. Plug-In Analytics </b>



- Breadth first search (BFS): analytic_bfs

```bash

analytic_bfs --graph <graph_name> --id <root_vid> [--depth <num_hops>]
[--width <max_breadth_per_level>]

```



`--id` specifies the ID of the vertex from which BFS starts. `--depth`
constrains the maximum number of levels for BFS. `--width` specifies the
maximum number of vertices to traverse at each BFS level. This is for
visualization purpose, where we do not want to visualize all the edges of the
vertices when they have a large number of neighbors. If `--depth` or `--width`
are not specified, all vertices will be traversed.



- Collaborative filtering: analytic_colfilter

```bash

analytic_colfilter --graph <graph_name> --id <root_vid> [--depth <num_hops>]
[--topnum <rank>]

```



Collaborative filtering is widely used in recommendation systems and has many
variations. In this version, it takes an undirected bipartite graph G((X, Y),
E) as input, and a vertex specified by `--id`, say x∈X. The analytic performs
BFS as above up to `--depth` (must be an even number, default to 4), computes
the number of paths N(x, y) from x to every vertex in Y and ranks these
vertices based on their N(x, y) values in a descending order. The top-ranked
vertices up to the value specified by `--topnum` (must be at least 10, default
to 100) are returned.



- PageRank: analytic_pagerank

```bash

analytic_pagerank --graph <graph_name> [--damp <damping_factor>]
[--quad <quadratic_error>] [--num <max_num_iterations>]
[--prop <vertex_prop_name_to_store_result>] [ --restart]

```



This analytic performs persistent PageRank in a directed graph. By persistent
PageRank, we mean that the importance value of each vertex is stored in each
iteration as a vertex property (specified by `--prop`). Thus, we can
incrementally perform PageRank at any time, or after any changes to the
graph. Given a directed graph G(V, E), the analytic works by counting the
number and quality of edges to a vertex to determine a rough estimate of how
important the vertex is in the graph. The quality is iteratively computed by:
PR(v_i) = (1-d)/N + d ∑<sub>{v_j∈ neighbors(v_i)}</sub> PR(v_j)/L(v_j), where
N=|V|; d is the damping factor and L(v_j) is the number of outgoing edges of
vertex v_j. The underlying assumption is that more important websites are
likely to be linked by other websites. The arguments for the command are the
damping factor `--damp` (default to 0.8), the quadratic error bound `--quad`
(default to 0.001), the maximum number of iterations `--num` (default 100),
and the initialization control `--restart`. The damping factor and quadratic
error are explained in Wikipedia. If `--restart` is specified, the analytic
re-initializes the importance of each vertex; otherwise, the currently stored
values are used. Note that due to a lot of string to number conversions, the
performance might be adversely impacted. For high-performance PageRank, a
separate in-memory PageRank subroutine is provided outside gShell.



- Auction: analytic_auction

```bash
analytic_auction --graph <graph_name> --prop <edge_prop_name_for_weight>
[--eps <epsilon>] [--num <max_num_iterations>] [--bipartite_check]
```


This analytic performs auction algorithm to find a maximum weight matching in
a weighted bipartite graph. If `--eps` is not specified, the default value
of 0.01 is used. If `--num` is not specified, the default value of 100 is
used. If `--bipartite_check` is specified, the analytic first checks whether
the graph is a directed bipartite graph.



- Analytic engine.

Analytic engine provides a number of graph analytics, which can be categorized
into three groups: (1) graph-level analytics including connected component,
k-core, betweenness centrality; (2) vertex-level analytics including
clustering coefficient, triangle count, degree centrality, closeness
centrality; (3) path analytics including shortest paths, top-k shortest paths,
find path.



- Start analytic engine: analytic_start_engine

```bash
analytic_start_engine --graph <graph_name>
[--edgeweightpropname <edge_prop_name_for_weight>] [--restart]
```



To run all the analytics provided by the analytic engine against a graph
store, the engine needs to be started first for this graph store in order to
pre-process graph information and initialize the in-memory data structures
used for the computation. The engine only needs to be started once for all the
analytics during a single gShell session. To run analytics that require edge
weights (e.g. analytics that require calculation of shortest paths between
vertices), `--edgeweightpropname` needs to be specified.

When this command is run for the first time on a graph store, it traverses the
whole graph to populate an in-memory representation of graph topology
information (vertices, edges with weights), and also persists the
representation in the graph store. Subsequent execution of this command (in a
later gShell session) will load the on-disk representation into memory instead
of traversing the graph again (unless `--restart` is specified), which will
significantly speed up the engine start time for a large graph.

To force recreation of the in-memory and on-disk representations by traversing
the graph again (e.g. when the graph is updated resulting in changes to
topology and/or edge weights), use the --restart argument. Because the
analytic engine will be started automatically when an analytic command is
issued, it is not necessary to issue this command explicitly unless
`--edgeweightpropname` or `--restart` is needed.

- Stop analytic engine: analytic_stop_engine

```bash
analytic_stop_engine --graph <graph_name>
```

This command stops the engine for a graph in order to release the memory.



- Reset analytic engine: analytic_reset_engine

```bash
analytic_reset_engine --graph <graph_name>
```



If the same analytic command is run multiple times on the same graph during a
single gShell session, certain in-memory data structures need to be reset to
ensure the correctness of the analytic result. The following command is used
to reset the engine. Note that this command doesn’t recompute the
representations used for graph topology information; use ` --restart` of
`analytic_start_engine` for this purpose.



- Whole-graph analytics. This set of analytics, including component, k-core
  and betweenness centrality, compute based on all vertices and edges of a
  graph. The input can be the whole graph stored in a graph store (specified
  in `--graph`) , or a sub-graph created by a previous command over a graph
  store (using `--graph` together with `--in`). If the sub-graph contains both
  vertices and edges, the computation is constrained to this sub-graph
  only. If the sub-graph only contains vertex information, the computation is
  based on the whole graph but the output is constrained to the set of
  vertices in the sub-graph.



- Connected component: analytic_connected_component



```bash
analytic_connected_component --graph <graph_name> [--in <cache_name>]
```

This analytic finds all connected components in a graph. The edges in the
graph are treated as undirected and edge weights are ignored. By default, the
component label of each vertex is written to the graph store as a vertex
property “analytic_component”, unless `--redirect` is used to redirect output
to an external file.



- K-core decomposition: analytic_k_core

```bash

analytic_k_core --graph <graph_name> --k <k> [--in <cache_name>]
[--out <cache_name>]

```



This analytic finds the k-core of a graph, where k is a parameter specified
using `--k`. A k-core of a graph G is a maximal connected subgraph of G in
which all nodes have degree at least k. The edges in the graph are treated as
undirected and edge weights are ignored. The output is one or more sub-graphs
each containing all the vertices that belong to a k-core and all the edges
between these vertices. `--out` can be used to save the output for use as the
input of other analytics.



- Betweenness centrality: analytic_betweenness_centrality

```bash

analytic_betweenness_centrality --graph <graph_name> [--ignoreedgeweight]
[--in <cache_name>]

```



This analytic computes the betweenness centrality of every vertex in the
graph. It is based on the algorithm described in "A faster algorithm for
betweenness centrality" by Ulrik Brandes. The shortest paths between a vertex
and any other vertex in the graph are calculated using Dijkstra’s algorithm,
taking edge weight into consideration unless `--ignoreedgeweight` is
specified. Due to the computational complexity of all-pair shortest paths
required to compute betweenness centrality, this analytic is recommended only
for small graphs. By default, the betweenness centrality of each vertex is
written to the graph store as a vertex property “analytic_betweenness”, unless
`--redirect` is used to redirect output to an external file.



- Vertex-level analytics. This set of analytics, including clustering
  coefficient, triangle count, degree centrality and closeness centrality,
  compute at the vertex level based on information local to each vertex. Like
  graph-level analytics, the input can be the whole graph stored in a graph
  store (specified in `--graph`) , or a sub-graph created by a previous
  command over a graph store (using `--graph` together with `--in`). If the
  sub-graph contains both vertices and edges, the computation is constrained
  to this sub-graph only. If the sub-graph only contains vertex information,
  the computation is based on the topology of the whole graph but the output
  is constrained to the set of vertices in the sub-graph. Different from
  graph-level analytics, `--id` is supported by all vertex-level analytics
  except degree centrality to only compute for a single vertex given its
  ID. If not specified, all vertices in the graph (or sub-graph) are
  computed. By default, the vertex-level analytic result of each vertex is
  written to the graph store as a vertex property
  (e.g. “analytic_coefficient”, “analytic_triangle”, “analytic_degree”,
  “analytic_closeness”) , unless `--redirect` is used to redirect output to an
  external file.



- Clustering coefficient: analytic_clustering_coefficient

```bash

analytic_clustering_coefficient --graph <graph_name> [--id <vertex_id>]
[--in <cache_name>]

```



This analytic computes the local clustering coefficient of each vertex. Let N
be the neighborhood of a vertex (immediately connected neighbors), let n be
|N|, i.e. size of N. The local clustering coefficient C of this vertex is the
number of links between the vertices within N divided by n*(n-1) for a
directed graph or n*(n-1)/2 for an undirected graph.





- Triangle count: analytic_triangle_count

```bash

analytic_triangle_count --graph <graph_name> [--id <vertex_id>]
[--in <cache_name>]

```



This analytic computes the triangle count on each vertex of an undirected or
directed graph. For a directed graph, it counts the total number of in-, out-,
through-, and cycle-triangles separately.





- Degree centrality: analytic_degree_centrality

```bash

analytic_degree_centrality --graph <graph_name> [--in <cache_name>]

```



This analytic computes the degree centrality of each vertex (total degree for
an undirected graph, in degree and out degree for a directed graph). Since
degree centrality is trivial and highly efficient to compute for every vertex,
`--id` is not needed.



- Closeness centrality: analytic_closeness_centrality

```bash

analytic_closeness_centrality --graph <graph_name> [--ignoreedgeweight]
[--id <vertex_id>] [--in <cache_name>]

```



This analytic computes the closeness centrality for each vertex. It uses the
Opsahl 2010 formula: C(i) = sum(1/shortest_distance(i, j)) for all j != i. The
shortest distance between a vertex and any other vertex in the graph is
calculated using Dijkstra’s algorithm, taking edge weight into consideration
unless `--ignoreedgeweight` is specified.



- Path analytics. This set of analytics, including shortest paths, top-k
  shortest paths and find path, compute paths between a pair of vertices. The
  input can be the whole graph stored in a graph store (specified in
  `--graph`) , or a sub-graph created by a previous command over a graph store
  (using `--graph` together with `--in`). The result is output to screen
  unless `--redirect` is used to redirect output to an external file.



- Shortest paths: analytic_shortest_paths

```bash

analytic_shortest_paths --graph <graph_name> [--src <src_vid>]
[--sink <sink_vid>] [--ignoredgeweight] [--hidepath] [--in <cache_name>]

```



This analytic computes the top shortest paths (of equal distance) between any
pair of vertices. If both `--src` and `--sink` are specified, single-pair
shortest paths are computed. If only `--src` is specified but no `--sink`,
single-source shortest paths (from the source vertex to all other vertices)
are computed. If only `--sink` is specified but no `--src`, single-sink
shortest paths (from all other vertices to the sink vertex) are computed. If
neither `--src` nor `--sink` is specified, all-pair shortest paths are
computed. When `--ignoreedgeweight` is specified, BFS is used for
single-source, single-sink, or all-pair shortest paths, and bi-directional BFS
is used for single-pair shortest paths. Note that bi-directional BFS finds one
or more shortest paths of equal length, but does not guarantee to find all
shortest paths between a pair of vertices. When `--ignoreedgeweight` is not
specified, Dijkstra’s algorithm is used, which finds all shortest paths of
equal distance between a pair of vertices. Use `--hidepath` if only a summary
of shortest paths is needed (which includes path length/distance and number of
paths) but not detailed paths.



- Top-k shortest paths: analytic_k_shortest_paths

```bash

analytic_k_shortest_paths --graph <graph_name> --src <src_vid> --sink
<sink_vid> --k <k> [--ignoredgeweight] [--hidepath] [--in <cache_name>]

```



This analytic computes top-k shortest loopless paths with non-negative edge
weights between a pair of vertices. It is based on Yen’s algorithm, optimized
to reduce redundant computation. `--k`, `--src` and `--sink` are required
arguments. When `--ignoreedgeweight` is specified, bi-directional BFS is used
as the base algorithm for the shortest path computation required by the Yen’s
algorithm; otherwise, Dijkstra’s algorithm is used.



- Find path: analytic_find_path

```bash

analytic_find_path --graph <graph_name> --src <src_vid> [--sink <sink_vid>]
[--maxnumhops <num_hops>] [--label <edge_label>] [--in <cache_name>]

```



This analytic uses BFS to find a path between a source vertex and a sink
vertex or any other vertex, with the optional constraints that the max number
of hops on the path cannot exceed the value of `--maxnumhops` and/or that all
edges on the path must have the same label value as specified by `--label`.


<b> 5. Plug-In Indexer </b>

- A third party indexer can be used for indexing vertices and edges based on
  their properties. We provide a simple command to inovke CLucene (2.3.2) indexer. The
  index must be used for a particular graph `<graph_name>`, specific type
  (this indexing is for vertex or edge) and the mode of the current invocation
  (build an index, or query from a built index). Thus, we can build indexings
  for vertex/edges based on different subproperties, and perform the query accordingly.

```bash
         indexer_clucene --graph <graph_name> --type <vertex|edge> --mode <build|query> --prop <subproperty_name> --term <term to match>
```
 
<b> 6. PLugin-In Geospatial Support</b>

- gShell can process geo-spatial information in Well-Known-Text ((WKT)[http://en.wikipedia.org/wiki/Well-known_text]) format.

```bash
  geo_contains --graph test2 --src v1 --depth 1 --contained "BOUNDINGBOX
  (-74.047285 40.6795479, -73.907 40.882214)" --geoloc "LOC"
  geo_contains --graph test2 --src v1 --depth 1 --contained "BOUNDINGBOX
  (-123.5337 36.8931, -121.9435 38.8643)" --geoloc "LOC"
  geo_contains --graph test2 --src v1 --depth 3 --contained "POINT
  (-122.41494 37.78745)" --geoloc "LOC"
  geo_intersects --graph test2 --src v1 --targ v10  --geoloc "LOC"
  geo_distance --graph test2 --src v1 --targ v10  --geoloc "LOC"
  geo_distance --graph test2 --src v1 --targ v5  --geoloc "LOC"
```




- BFS on vertices contained in a bounding box `geo_contains`. In this command,
`--src` specifies the ID of the vertex at which the BFS starts. `--depth`
constrains the maximum number of levels (hops). `--contained` specifies the
geometry (in (WKT)[http://en.wikipedia.org/wiki/Well-known_text] format) used
to specify a bounding-box condition. That is BFS returns those vertices that
satisfy the “contains” condition. `--geoloc` specifies the property name that
specifies the location property in the graph.

```bash
geo_contains --graph <graph_name> --src <root_vid> [—depth <num_hops>]
—contained “<WKT string>” --geoloc “geo_property_name”
```

Example vertex csv:
```
ID,WEIGHT,TAG,INFO,LOC
v1,0.5,A,aa,"POINT (-122.41823 37.78689)"
...
v10,0.3,C,aa,"POINT (-122.41823 37.78689)"
```

- We have a command `geo_contains` to check if a vertex is contained in a
  user-defined polygon. An example and the output are:

```bash
geo_contains --graph test2 --src v1 --depth 1 --contained "BOUNDINGBOX
(-123.5337 36.8931, -121.9435 38.8643)" --geoloc "LOC"
{
"time":[{"TIME":"0.000216007"}],
"vertex":[{"id":"v2"}]
}
```

- A command to check if two vertices intersect, invoked by `geo_intersects`,
where `--src` specifies the ID of the vertex/edge 1 for which intersection
check is performed `--targ` specifies the ID of the vertex/edge 2 for which
intersection check is performed

```bash
geo_intersects --graph <graph_name> --src v1 --targ v10  --geoloc
"geo_property_name"
```
Example:

```bash
geo_intersects --graph test2 --src v1 --targ v10  --geoloc "LOC"
{
"time":[{"TIME":"7.60555e-05"}],
"vertex":[{"id":"v1 INSTERSECTS v10"}]
}
```

- Distance of one geometry in another:

```bash
geo_distance --graph <graph_name> --src v1 --targ v10 --geoloc
"geo_property_name"
```

Here is the example and sample output:
```bash
geo_distance --graph test2 --src v1 --targ v5  --geoloc "LOC"
{
"distance":[{"v1 -> v5":"1355.00467"}],
"time":[{"TIME":"7.51019e-05"}]
}
```



<b> 7. Multi-User Support </b>

gShellSuperMgr is used for the server-side processing of gShell in multi-user
mode. gShellClientMulti is used by the client to communicate with the
server. In addition to the gShell commands described in the earlier sections,
there are several additional commands supported by gShellSuperMgr to manage
users.



- Register a user

```bash

./gShellClientMulti “register <username> <password>” <username> <server_ip>
<socket_port>

```



- Login a user

```bash

./gShellClientMulti “login <username> <password>” <username> <server_ip>
<socket_port>

```

- Logout a user

```bash

./gShellClientMulti “logout <username>” <username> <server_ip> <socket_port>

```



- Check the status a user (active or inactive)

```bash

./gShellClientMulti “check_user <username>” <username> <server_ip>
<socket_port>

```



- List all registered users and the port number assigned to each for
  communicating with gShell server

```bash

./gShellClientMulti “list_users” admin <server_ip> <socket_port>

```

A port number of 0 means that the user is inactive (logged out).



- Get the number of active users

```bash

./gShellClientMulti “num_users” admin <server_ip> <socket_port>

```



- Terminate gShellSuperMgr

```bash

./gShellClientMulti “bye” admin <server_ip> <socket_port>

```


