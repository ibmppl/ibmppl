<html>
<head>
<title>Documentation of IBM System G Native Graph Store gShell</title>
</head>
<body>
<a name="top"></a>
<table width="100%">
  <tr>
    <td width="10%"></td>
	  <td><div id="greeting"></div></td>
	    </tr>
		  <tr>
		      <td width="10%"></td>
			      <td><center>

# Documentation of IBM System G Native Graph Store gShell<h1></center></td>
    </tr>
	  <tr>
	      <td width="10%"></td>
		      <td width="80%">

[Stat gShell](#start) |
[Overview](#overview) |
[Basic commands](#basic) |
[Indexer commands](#indexer) |
[Analytic commands](#analytic) |
[Multi-user support](#multi-user)

<a name="start"></a>
  <h2>Start gShell

To start gShell, go to app/gShell, type the following command before invoking
gShell:
<pre style="border:1px; background-color:#eeeeee">

  export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:../../lib/

</pre>

gShell can be invoked in any of the following modes:

### Interactive mode

<pre style="border:1px; background-color:#eeeeee">

  ./gShell interactive

</pre>
gShell displays a prompt ">>" waiting for input commands. To exit, type
_close_all_ or _Ctrl-c_.

### Batch mode

<pre style="border:1px; background-color:#eeeeee">

  ./gShell interactive < &lt;batch_file&gt; (e.g., ./gShell interactive <
  script.txt)

</pre>
The batch mode is a variant of the interactive mode, where the commands stored
in a text file _&lt;batch_file&gt;_ are redirected to the interactive mode
(using "<")
and executed sequentially. Note that _close all_ needs to be included as the
last command in the file in order exit from gShell.

### Single-user server/client mode

<pre style="border:1px; background-color:#eeeeee">

  ./gShell server &lt;socket_port&gt; (e.g., ./gShell server 9998)
    ./gShellClient &lt;server_ip&gt; "&lt;command+arguments&gt;"
    &lt;socket_port&gt; (e.g., ./gShellClient 127.0.0.1 "create --graph g
    --type undirected" 9998)

</pre>
The communication between server and client is through IPC socket.

### Multi-user server/client mode

<pre style="border:1px; background-color:#eeeeee">

  ./gShellSuperMgr 7755
    ./gShellClientMulti "&lt;command+arguments&gt;" &lt;username&gt;
    &lt;server_ip&gt; &lt;socket_port&gt; (e.g., ./gShellClientMulti "create
    --graph g --type undirected" user123 127.0.0.1 7755

</pre>
The multi-user mode allows multiple gShell instances to work concurrently, one
gShell instance per user.
gShellSuperMgr manages all gShell instances and coordinates client
communications from multiple users.
If the port number is not specified for gShellSuperMgr, the default port
number of 7755 is used.

[Back to top](#top)

<a name="overview"></a>

## Overview

All gShell commands share the same format:
<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  _command --arg1 value1 --arg2 value2_ ...

</pre>
Each command in gShell comes with an argument _--help_ for displaying the
argument information. Arguments can be specified in any order.
Those not marked as _[optional]_ are mandatory. Argument values containing
space must be quoted.

Commands in gShell can be categorized into two groups: shell operation
commands (including _help_, _list_all_, _close_all_, _version_),
and store operation commands. Store operation commands perform against a
particular graph store.
Since gShell can concurrently operate multiple graph stores, a store name must
be provided using the _--graph_ argument for these commands.

In the interactive mode, pressing the _tab_ key results in a list of all the
available commands to be displayed.
When in the middle of inputting a command, we can press _tab_ once for
auto-completing the input.
If the input is not unique given what we have typed in, we can press _tab_
twice to list all choices.
Similarly, we can request auto-completion of the arguments and file paths by
pressing _tab_.

By default, the output information is in JSON format, but we can request a
more human readable format by specifying _--format plain_ in each command.

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

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
													    list_all - list all
    graphs
	  <info>
	      MESSAGE
		      --format:  [optional] output format
			    <info>
				    MESSAGE
					    --help:  [optional] help infomation
						  ---------------------------------------

</pre>
</p>
Other common arguments include _--redirect_ to redirect shell output to a file
on disk,
_--out_ to cache the result of a command (in the format of vertex and edge
IDs),
_--in_ to use the cached result of a previous command as input, essentially
chaining together multiple commands
(i.e., the output of the first command becomes the input of the second command
and so on).
</p>

Below we describe the commonly used commands in gShell. Note that this
documentation discusses commonly used arguments for each command,
not necessarily the complete argument list. For the complete argument list of
each command, please use the _--help_ argument.

In this document, &lt;...&gt; is used to indicate the value of an argument,
e.g. _&lt;graph_name&gt;_.
Any argument in [...] is optional. {...} indicates the set of possible values
for an argument. (...|...) indicates that one of the enclosed arguments needs
to be specified.

[Back to top](#top)

<a name="basic"></a>

## Basic Commands

### Create a store: _create_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  create --graph &lt;graph_name&gt; [--type &lt;{undirected, directed}&gt;]

</pre>
If _--type_ is not specified, a directed graph is created by default. Note
that the graph in a graph store is not necessarily connected;
that is, a graph store can maintain a set of small graphs, but all of them
must be of the same type (directed, or undirected).

### Populate a store: _load_csv_vertices_, _load_csv_edges_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  load_csv_vertices --graph &lt;graph_name&gt; --csvfile
  &lt;vertex_csv_file&gt; --keypos &lt;col#_vid&gt;
  [--labelpos &lt;col#_label&gt;] [--label &lt;vertex_label&gt;] [--no_header]
  [--separator &lt;,&gt;]
    load_csv_edges --graph &lt;graph_name&gt; --csvfile &lt;edge_csv_file&gt;
  --srcpos &lt;col#_src&gt; --targpos &lt;col#_targ&gt;
  [--labelpos &lt;col#_label&gt;] [--label &lt;edge_label&gt;] [--no_header]
  [--separator &lt;,&gt;]

</pre>
After the _create_ command is executed, we have _&lt;graph_name&gt;_ as an
empty graph store.
An easy way to populate the store is to import vertex and edge information
from files.

Each line in the vertex csv file provides information about one
vertex. _--keypos_ specifies the column number
(starting from 0) in the vertex csv file that corresponds to the ID of each
vertex, _--labelpos_ provides the column number for the label of each vertex,
and the rest of the columns specify the properties of each vertex as a vector
of strings.

Each line in the edge csv file provides information about one edge.
_--srcpos_ and _--targpos_ indicate the respective column numbers (starting
from 0) in the edge csv file that
correspond to the source and target vertex IDs of each edge, _--labelpos_
provides the column number for the label of each edge,
and the data in the rest of the columns are treated as the properties of each
edge.

Note that "_label_", "_exid_", and "_vclass_" (case sensitive) are reserved
for internal use and should not be used as property names.
An alternative to _--labelpos_ is _--label_, which provides a label to be
applied to all the vertices or edges in the file.

If the csv file has no header, then we must specify _--no_header_. gShell
automatically recognizes the use of comma, tab or space to separate columns in
the csv file.
The separator (e.g. "_,_" or "_;_") is specified with _--separator_
(optional).
If the string value of this argument contains multiple characters, each
character is treated as a separator.

Multiple vertex or edge csv files can be loaded to a single graph store, which
allows vertex or edge with different types and properties to be supported.
Note that multiple occurrences of the same (source, target) pair are treated
as multiple edges.

### Update a store: _add_vertex_, _add_edge_, _update_vertex_, _update_edge_,
    _delete_vprop_, _delete_eprop_, _delete_vertex_, _delete_edge_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  add_vertex --graph &lt;graph_name&gt; --id &lt;vertex_id&gt;
  [--prop &lt;name1:value1 name2:value2 ...&gt;]
  [--label &lt;vertex_lable&gt;]
    add_edge --graph &lt;graph_name&gt; --src &lt;src_vid&gt; --targ
  &lt;targ_vid&gt; [--prop &lt;name1:value1 name2:value2 ...&gt;]
  [--label &lt;edge_label&gt;]
    update_vertex --graph &lt;graph_name&gt; --id &lt;vertex_id&gt; --prop
  &lt;name1:value1 name2:value2 ...&gt;
    update_edge --graph &lt;graph_name&gt; --src &lt;src_vid&gt; --targ
  &lt;targ_vid&gt; --prop &lt;name1:value1 name2:value2 ...&gt;
  [--label &lt;edge_label&gt;] [--eid &lt;edge_id&gt;]
    delete_vprop --graph &lt;graph_name&gt; --id &lt;vertex_id&gt; --prop
  &lt;name1 name2 ...&gt;
    delete_eprop --graph &lt;graph_name&gt; --src &lt;src_vid&gt; --targ
  &lt;targ_vid&gt; --prop &lt;name1 name2 ...&gt; [--label &lt;edge_label&gt;]
  [--eid &lt;edge_id&gt;]
    delete_vertex --graph &lt;graph_name&gt; --id &lt;vertex_id&gt;
	  delete_edge --graph &lt;graph_name&gt; --src &lt;src_vid&gt; --targ
  &lt;targ_vid&gt; [--eid &lt;edge_id&gt;]

</pre>
Multiple values of _--prop_ are separated by space. Property name or value
containing space must be quoted.
The number of properties for vertices and edges is arbitrary (0 to 2^64). If
there are multiple edges between a pair of vertices,
use _--eid_ to specify a particular edge. _--label_ is used to filter to
edge(s) of a specific label. Otherwise, all the edges are affected.

Note that currently update to vertex or edge label is not
supported. Therefore, the labels can only be set when _load_csv_vertices_,
_load_csv_edges_,
_add_vertex_, or _add_edge_ are called with the _--label_ or _--labelpos_
arguments.

Examples:
<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  add_vertex --graph g --id John --prop memo:"These are my desk, table, and
  chair" income:1000.00 --label person
    add_edge --graph g --src Mary --targ John --prop memo:"They are friends"
  time:"2011-11-11"
    update_vertex --graph g --id John --prop memo:"These are my books and
  laptop"
    update_edge --graph g  --src Mary --targ John --prop memo:"They are close
  friends" time:"2011-12-12"
    delete_vprop --graph g --id John --prop memo
	  delete_eprop --graph g --src Mary --targ John --prop memo time
	    delete_vertex --graph g --id John
		  delete_edge --graph g --src Mary --targ John

</pre>

### Open a store: _open_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  open --graph &lt;graph_name&gt;

</pre>

 Opening a store loads the essential information needed for graph access from
 disk to memory. The rest of the graph is loaded into memory on demand
 according to the requirements of each individual command. When a command is
 issued against a particular graph store, the store is automatically opened if
 not already. Therefore, it is not necessary to use this command explicitly.

### Save/close a store: _close_, _close_all_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  close --graph &lt;graph_name&gt;
    close_all

</pre>

Closing a store persists it on disk and removes the store from memory, so that
we have more memory to process other graphs.
Or, we can use _close_all_ to close all opened graphs in order to release
memory. gShell captures _Ctrl-c_ and interpret it as the _close_all_ command.

Note that the _close_ command must be used if the graph store is to be
persisted on disk and loaded into memory at a later time.

### List all stores and their types: _list_all_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  list_all

</pre>

This command will list all existing stores (opened or not opened) and their
respective graph types (directed, undirected). Note that this command will not
load (open) any store if they are not opened already.

### Erase a store from the disk: _delete_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  delete --graph &lt;graph_name&gt;

</pre>

This is a permanent deletion and cannot be recovered. Therefore, this command
should be used with caution.

### Print a store: _print_all_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  print_all --graph &lt;graph_name&gt; [--in &lt;cache_name&gt;]
  [--outputtype &lt;{vertex, edge, all (default)}&gt;] [--id_only]
  [--format &lt;{json, plain, vertexcsv, edgecsv, internal}&gt;]

</pre>

This command prints all vertices and/or edges (depending on the value of
_--outputtype_) with or without properties (depending on the absence/presence
of _--id_only_)
of the whole graph from a graph store, or the sub-graph stored in
_&lt;cache_name&gt;_.
It is not recommended to use for large graphs.
If _--format vertexcsv_ is specified, only vertex information is displayed in
csv format.
Similarly, if _--format edgecsv_ is specified, only edge information is
displayed in csv format.
</p>

### Export a store to external csv files: _export_csv_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  export_csv --graph &lt;graph_name&gt; --path &lt;directory&gt;

</pre>

If there are different types of vertices with different sets of properties,
gShell creates one vertex csv file for each type of vertices.
Similarly, if there are different types of edges with different sets of
properties, gShell creates one edge csv file for each type of edges.
As a result, multiple vertex/edge csv files may be created in the
_&lt;directory&gt;_.

### Get the size of a store: _get_num_vertices_, _get_num_edges_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  get_num_vertices --graph &lt;graph_name&gt; [--in &lt;cache_name&gt;]
    get_num_edges --graph &lt;graph_name&gt; [--in &lt;cache_name&gt;]

</pre>

If _--in_ is used, the computation is based on the subgraph stored in
_&lt;cache_name&gt;_ as the result of a previously issued command.

### Get all information about vertex or edge: _find_vertex_, _find_edge_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  find_vertex --graph &lt;graph_name&gt; ([--id &lt;vertex_id&gt;] |
  [--in &lt;cache_name&gt;]) [--out &lt;cache_name&gt;]
    find_multiple_vertex --graph &lt;graph_name&gt; --id &lt;vertex_id1
  vertex_id2 ...&gt; [--out &lt;cache_name&gt;]
    find_edge --graph &lt;graph_name&gt; ([--src &lt;src_vid&gt;]
  [--targ &lt;targ_vid&gt;] [--eid &lt;edge_id&gt;] |
  [--in &lt;cache_name&gt;]) [--label &lt;edge_label&gt;]
  [--out &lt;cache_name&gt;]

</pre>

For _find_vertex_, the input comes from either _--id_ for a single vertex or
_--in_ for a set of vertices.
For _find_edge_, the input comes from either _--src_ and _--targ_ or _--in_.
_--eid_ is used in combination with _--src_ and _--targ_ to get a particular
edge when there may be multiple edges between them.
_--label_ is used to filter to edges with a particular label.

### Find the vertex with the maximum degree (number of neighbors):
    _find_vertex_max_degree_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  find_vertex_max_degree --graph &lt;graph_name&gt;
  [--edgetype &lt;{in, out, all (default)}&gt;]

</pre>

If there are multiple such vertices, only one is returned.

### Get neighbor information of vertex: _get_vertex_degree_, _find_neighbors_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  get_vertex_degree --graph &lt;graph_name&gt; --id &lt;vertex_id&gt;
  [--edgetype &lt;{in, out, all (default)}&gt;]
    find_neighbors --graph &lt;graph_name&gt; ([--id &lt;vertex_id&gt;] |
  [--in &lt;cache_name&gt;]) [--label &lt;edge_label&gt;]
  [--edgetype &lt;{in, out, all (default)}&gt;] [--id_only]
  [--out &lt;cache_name&gt;]

</pre>
For _find_neighbors_, the vertex information comes from either _--id_ or
_--in_.
If _--label_ is specified, gShell returns only neighbors whose edges between
them and the given vertex have the specified label.
If _--id_only_ is present, the result contains the identity information of
neighboring vertices/edges only without property information.

### Filter vertices or edges by label or property: _filter_vertices_,
    _filter_edges_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  filter_vertices --graph &lt;graph_name&gt;
  [--label &lt;label1 label2 ...&gt;] [--prop &lt;name1 name2 ...&gt;]
  [--condition "&lt;expression&gt;"]
    filter_edges --graph &lt;graph_name&gt;
  [--label &lt;label1 label2 ...&gt;] [--prop &lt;name1 name2 ...&gt;]
  [--condition "&lt;expression&gt;"]

</pre>

To filter by label (separate multiple labels by space), use _--label_.
To filter by existence of certain properties, use _--prop_ to specify the
names of the properties.
To filter by property values, use _--prop_ to specify the names of the
properties (separated by space),
and use _--condition_ to specify the expression (must be quoted) for
evaluating the values of the specified properties.

Examples:

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  filter_vertices --graph g --label A --prop tag
    filter_vertices --graph g --label A B --prop tag value --condition "tag==T
    || (value>0.3 && value < 0.9)"
	  filter_edges --graph g --label a --prop weight
	    filter_edges --graph g --label a b --prop weight --condition "weight
    <0.2 || weight > 0.7"

</pre>

### Get random vertices or edges: _find_random_vertices_, _find_random_edges_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  find_random_vertices --graph &lt;graph_name&gt; --num &lt;n&gt;
  [--out &lt;cache_name&gt;]
    find_random_edges --graph &lt;graph_name&gt; --num &lt;n&gt;
  [--out &lt;cache_name&gt;]

</pre>

These commands are useful for getting a sub-graph. _--num_ specifies the
number of vertices or edges returned.
Note that the result may contain duplicates. _--out_ is used to save the
result for later use.

### Get egonet of a vertex: _get_egonet_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  get_egonet --graph &lt;graph_name&gt; --id &lt;vertex_id&gt;
  [--depth &lt;num_hops&gt;] [--out &lt;cache_name&gt;]

</pre>
The K-hop egonet of a given vertex contains all the vertices and edges between
them within K hops from the vertex when breath first search is conducted
with the vertex as the root. Edge directions are ignored. If _--depth_ is not
specified, the default value of 1 is used.

### Get the induced subgraph given a list of vertices: _get_subgraph_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  get_subgraph --graph &lt;graph_name&gt;
  ([--id &lt;vertex_id1 vertex_id2 ...&gt;] | [--in &lt;cache_name&gt;])
  [--out &lt;cache_name&gt;]

</pre>
The list of vertices is specified by _--id_ or _--in_. The induced subgraph
contains all the vertices in the list and all the edges between them.

[Back to top](#top)

<a name="indexer"></a>

## Indexer Commands

A third party indexer can be implemented as a plug-in to index vertex and edge
properties for enabling more quickly and comprehensive search capabilities on
properties.
We integrate CLucene (2.3.2) indexer with current gShell. Each index is built
for a single property of all of either vertices or edges in a single graph
store.

### Build an index on a vertex/edge property: _indexer_clucene --mode build_

<p>
<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  indexer_clucene --graph &lt;graph_name&gt; --type &lt;{vertex, edge}&gt;
  --mode build --prop &lt;prop_name&gt;

</pre>
Note that _&lt;prop_name&gt;_ needs to be present for all the vertices (or
edges) in order for the index to be built successfully.
Each string value of the property to be indexed is tokenized into terms using
the default Lucene tokenizer. Note that the index is case insensitive.

### Query an index already built on a vertex/edge property: _indexer_clucene
    --mode query_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  indexer_clucene --graph &lt;graph_name&gt; --type &lt;{vertex, edge}&gt;
  --mode query --prop &lt;prop_name&gt; --term &lt;lucene_query_terms&gt;

</pre>
_&lt;lucene_query_terms&gt;_ can include terms (case insensitive), wildcards
(*, ?), ranges (TO), Boolean operators (AND, OR, NOT) and grouping described
in
[Lucene query syntax](http://lucene.apache.org/core/2_9_4/queryparsersyntax.html).

[Back to top](#top)

<a name="analytic"></a>

## Analytic Commands

### Breadth first search (BFS): _analytic_bfs_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  analytic_bfs --graph &lt;graph_name&gt; --id &lt;root_vid&gt;
  [--depth &lt;num_hops&gt;] [--width &lt;max_breadth_per_level&gt;]

</pre>

_--id_ specifies the ID of the vertex from which BFS starts. _--depth_
constrains the maximum number of levels (hops) for BFS.
_--width_ specifies the maximum number of vertices to traverse at each BFS
level.
This is for visualization purpose, where we do not want to visualize all the
edges of the vertices when they have a large number of neighbors.
If _--depth_ or _--width_ are not specified, all vertices will be traversed.

### Collaborative filtering: _analytic_colfilter_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  analytic_colfilter --graph &lt;graph_name&gt; --id &lt;root_vid&gt;
  [--depth &lt;num_hops&gt;] [--topnum &lt;rank&gt;]

</pre>

Collaborative filtering is widely used in recommendation systems and has many
variations.
In this version, it takes an undirected bipartite graph G((X, Y), E) as input,
and a vertex specified by _--id_, say x in X.
The analytic performs BFS as above up to _--depth_ (must be an even number,
default is 4), computes the number of paths N(x, y) from x to every vertex in
Y, and
ranks these vertices based on their N(x, y) values in a descending order.
The top-ranked vertices up to the value specified by _--topnum_ (must be at
least 10, default is 100) are returned.

### PageRank: _analytic_pagerank_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  analytic_pagerank --graph &lt;graph_name&gt; [--damp &lt;damping_factor&gt;]
  [--quad &lt;quadratic_error&gt;] [--num &lt;max_num_iterations&gt;]
  [--prop &lt;vertex_prop_name_to_store_result&gt;] [--restart]

</pre>

This analytic performs persistent PageRank in a directed graph.
By persistent PageRank, we mean that the importance value of each vertex in
each iteration is stored as a vertex property (specified by _--prop_).
Thus, we can incrementally perform PageRank at any time, or after any changes
to the graph.

Given a directed graph G(V, E), the analytic works by computing iteratively
the number and quality of edges to a vertex to determine a rough estimate of
how important the vertex is in the graph.
The arguments for the command are the damping factor _--damp_ (default
is 0.8),
the quadratic error bound _--quad_ (default is 0.001), the maximum number of
iterations _--num_ (default is 100), and the initialization control
_--restart_.
The algorithm and the arguments are explained in
[Wikipedia](http://en.wikipedia.org/wiki/PageRank).
If _--restart_ is specified, the analytic re-initializes the importance of
each vertex;
otherwise, the currently stored values are used.

Note that due to a lot of string to number conversions, the performance might
be adversely impacted.
For high-performance PageRank, a separate in-memory PageRank subroutine is
provided outside gShell.

### Auction: _analytic_auction_

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  analytic_auction --graph &lt;graph_name&gt; --prop
  &lt;edge_prop_name_for_weight&gt; [--eps &lt;epsilon&gt;]
  [--num &lt;max_num_iterations&gt;] [--bipartite_check]

</pre>

This analytic performs
[auction algorithm](http://en.wikipedia.org/wiki/Auction_algorithm) to find a
maximum weight matching in a weighted bipartite graph.
If _--eps_ is not specified, the default value of 0.01 is used. If _--num_ is
not specified, the default value of 100 is used.
If _--bipartite_check_ is specified, the analytic first checks whether the
graph is a directed bipartite graph.

### Geospatial support: _geo_contains_ (available only in some packages)

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  geo_contains --graph &lt;graph_name&gt; --src &lt;root_vid&gt; --depth
  &lt;num_hops&gt; --contained "&lt;WKT string&gt;" --geoloc
  "&lt;vertex_prop_name_for_geo_location&gt;"

</pre>

This analytic performs BFS from a root vertex and returns all vertices
contained in a bounding box. _--src_ specifies the ID of the vertex from which
the BFS starts (root).
_--depth_ constrains the maximum number of levels (hops) for BFS.
_--contained_ specifies the geometry (in WKT format) used to specify the
bounding-box.
_--geoloc_ specifies the vertex property name that specifies the location.

Here is an example:

<pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
word-wrap: break-word;">

  geo_contains --graph test2 --src v1 --depth 1 --contained "BOUNDINGBOX
  (-123.5337 36.8931, -121.9435 38.8643)" --geoloc "LOC"

</pre>

### <font color="brown">Analytic engine</font>

Analytic engine provides a number of graph analytics, which can be categorized
into three groups:

1.  graph-level analytics including connected component, k-core, betweenness
    centrality
	2.  vertex-level analytics including clustering coefficient, triangle
        count, degree centrality, closeness centrality
		3.  path analytics including shortest paths, top-k shortest paths,
            find path

#### Start analytic engine: _analytic_start_engine_

  <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
  word-wrap: break-word;">

  analytic_start_engine --graph &lt;graph_name&gt;
  [--edgeweightpropname &lt;edge_prop_name_for_weight&gt;] [--restart]
    </pre>

To run all the analytics provided by the analytic engine against a graph
store, the engine needs to be started first for this graph store in order to
pre-process graph information and
initialize the in-memory data structures used for the computation. The engine
only needs to be started once for all the analytics during a single gShell
session.

To run analytics that require edge weights (e.g. analytics that require
calculation of shortest paths between vertices), _--edgeweightpropname_ needs
to be specified.

When this command is run for the first time on a graph store, it traverses the
whole graph to populate an in-memory representation of graph topology
information
(vertices, edges with weights), and also persists the representation in the
graph store.
Subsequent execution of this command (in a later gShell session) will load the
on-disk representation into memory instead of traversing the graph again
(unless _--restart_ is specified),
which will significantly speed up the engine start time for a large graph.

To force recreation of the in-memory and on-disk representations by traversing
the graph again (e.g. when the graph is updated resulting in changes to
topology and/or edge weights),
use the _--restart_ argument. Because the analytic engine will be started
automatically when an analytic command is issued,
it is not necessary to issue this command explicitly unless
_--edgeweightpropname_ or _--restart_ is needed.

#### Stop analytic engine: _analytic_stop_engine_

  <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
  word-wrap: break-word;">

  analytic_stop_engine --graph &lt;graph_name&gt;
    </pre>
	This command stops the engine for a graph in order to release the memory.

#### Reset analytic engine: _analytic_reset_engine_

  <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
  word-wrap: break-word;">

  analytic_reset_engine --graph &lt;graph_name&gt;
    </pre>

If the same analytic command is run multiple times on the same graph store
during a single gShell session,
certain in-memory data structures need to be reset to ensure the correctness
of the analytic result.
Note that this command doesn't recompute the representations used for graph
topology information;
use _--restart_ of _analytic_start_engine_ for this purpose.

#### <font color="brown">Whole-graph analytics</font>

This set of analytics, including component, k-core and betweenness centrality,
compute based on all vertices and edges of a graph.
  The input can be the whole graph stored in a graph store (specified in
  _--graph_), or a sub-graph created by a previous command over a graph store
    (using _--graph_ together with _--in_). If the sub-graph contains both
	vertices and edges, the computation is constrained to this sub-graph
	only.
	  If the sub-graph only contains vertex information, the computation is
	  based on the whole graph but the output is constrained to the set of
	  vertices in the sub-graph.

#### Connected component: _analytic_connected_component_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_connected_component --graph &lt;graph_name&gt;
  [--in &lt;cache_name&gt;]
      </pre>
	  This analytic finds all connected components in a graph. The edges in
  the graph are treated as undirected and edge weights are ignored.
  By default, the component label of each vertex is written to the graph store
  as a vertex property "_analytic_component_",
  unless _--redirect_ is used to redirect output to an external file.

#### K-core decomposition: _analytic_k_core_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_k_core --graph &lt;graph_name&gt; --k &lt;k&gt;
  [--in &lt;cache_name&gt;] [--out &lt;cache_name&gt;]
      </pre>

This analytic finds the k-core of a graph, where k is a parameter specified
using _--k_.
A k-core of a graph G is a maximal connected subgraph of G in which all
vertices have degree at least k.
The edges in the graph are treated as undirected and edge weights are
ignored.
The output is one or more sub-graphs each containing all the vertices that
belong to a k-core and all the edges between these vertices.
_--out_ can be used to save the output for use as the input of other
analytics.

#### Betweenness centrality: _analytic_betweenness_centrality_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_betweenness_centrality --graph &lt;graph_name&gt;
  [--ignoreedgeweight] [--in &lt;cache_name&gt;]
      </pre>

This analytic computes the betweenness centrality of every vertex in the
graph.
It is based on the algorithm described in "_A faster algorithm for betweenness
centrality_" by Ulrik Brandes.
The shortest paths between a vertex and any other vertex in the graph are
calculated using Dijkstra's algorithm,
taking edge weights into consideration unless _--ignoreedgeweight_ is
specified.
Due to the computational complexity of all-pair shortest paths required to
compute betweenness centrality,
this analytic is recommended only for small graphs. By default, the
betweenness centrality of each vertex is written to the graph store as a
vertex property "_analytic_betweenness_",
unless _--redirect_ is used to redirect output to an external file.

#### <font color="brown">Vertex-level analytics</font>

This set of analytics, including clustering coefficient, triangle count,
degree centrality and closeness centrality,
  compute at the vertex level based on information local to each vertex. Like
  graph-level analytics, the input can be the whole graph stored in a graph
  store
    (specified in _--graph_) , or a sub-graph created by a previous command
	over a graph store (using _--graph_ together with _--in_).
	  If the sub-graph contains both vertices and edges, the computation is
	  constrained to this sub-graph only.
	    If the sub-graph only contains vertex information, the computation is
		based on the topology of the whole graph but the output is constrained
		to the set of vertices in the sub-graph.
		  Different from graph-level analytics, _--id_ is supported by all
		  vertex-level analytics except degree centrality to only compute for
		  a single vertex given its ID.
		    If not specified, all vertices in the graph (or sub-graph) are
			computed.
			  By default, the vertex-level analytic result of each vertex is
			  written to the graph store as a vertex property
			  (e.g. "_analytic_coefficient_", "_analytic_triangle_",
			    "_analytic_degree_", "_analytic_closeness_"), unless
				_--redirect_ is used to redirect output to an external file.

#### Clustering coefficient: _analytic_clustering_coefficient_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_clustering_coefficient --graph &lt;graph_name&gt;
  [--id &lt;vertex_id&gt;] [--in &lt;cache_name&gt;]
      </pre>

 This analytic computes the local clustering coefficient of each vertex. Let N
 be the neighborhood of a vertex (immediately connected neighbors),
  let n be |N|, i.e. size of N. The local clustering coefficient C of this
 vertex is the number of links between the vertices within N divided by
 n*(n-1)
  for a directed graph or n*(n-1)/2 for an undirected graph.

#### Triangle count: _analytic_triangle_count_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_triangle_count --graph &lt;graph_name&gt; [--id &lt;vertex_id&gt;]
  [--in &lt;cache_name&gt;]

</pre>

This analytic computes the triangle count on each vertex of an undirected or
directed graph.
For a directed graph, it counts the total number of in-, out-, through-, and
cycle-triangles separately.

#### Degree centrality: _analytic_degree_centrality_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_degree_centrality --graph &lt;graph_name&gt;
  [--in &lt;cache_name&gt;]
      </pre>

This analytic computes the degree centrality of each vertex (total degree for
an undirected graph, in degree and out degree for a directed graph).
Since degree centrality is trivial and highly efficient to compute for every
vertex, _--id_ is not needed.
</p>

#### Closeness centrality: _analytic_closeness_centrality_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_closeness_centrality --graph &lt;graph_name&gt;
  [--ignoreedgeweight] [--id &lt;vertex_id&gt;] [--in &lt;cache_name&gt;]

</pre>

This analytic computes the closeness centrality for each vertex. It uses the
Opsahl 2010 formula: C(i) = sum(1/shortest_distance(i, j)) for all j != i.
The shortest distance between a vertex and any other vertex in the graph is
calculated using Dijkstra's algorithm,
taking edge weights into consideration unless _--ignoreedgeweight_ is
specified.

#### <font color="brown">Path analytics</font>

This set of analytics, including shortest paths, top-k shortest paths and find
path, compute paths between a pair of vertices.
  The input can be the whole graph stored in a graph store (specified in
  _--graph_) ,
    or a sub-graph created by a previous command over a graph store (using
	_--graph_ together with _--in_).
	  The result is output to screen unless _--redirect_ is used to redirect
	  output to an external file.

#### Shortest paths: _analytic_shortest_paths_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_shortest_paths --graph &lt;graph_name&gt; [--src &lt;src_vid&gt;]
  [--sink &lt;sink_vid&gt;] [--ignoredgeweight] [--hidepath]
  [--in &lt;cache_name&gt;]

</pre>

This analytic computes the top shortest paths (of equal distance) between any
pair of vertices. If both _--src_ and _--sink_ are specified,
single-pair shortest paths are computed. If only _--src_ is specified but no
_--sink_,
single-source shortest paths (from the source vertex to all other vertices)
are computed. If only _--sink_ is specified but no _--src_,
single-sink shortest paths (from all other vertices to the sink vertex) are
computed. If neither _--src_ nor _--sink_ is specified,
all-pair shortest paths are computed. When _--ignoreedgeweight_ is specified,
BFS is used for single-source, single-sink, or all-pair shortest paths,
and bi-directional BFS is used for single-pair shortest paths. Note that
bi-directional BFS finds one or more shortest paths of equal length,
but does not guarantee to find all shortest paths between a pair of
vertices. When _--ignoreedgeweight_ is not specified, Dijkstra's algorithm is
used,
which finds all shortest paths of equal distance between a pair of vertices.
Use _--hidepath_ if only a summary of shortest paths is needed
(which includes path length/distance and number of paths) but not detailed
paths.

#### Top-k shortest paths: _analytic_k_shortest_paths_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_k_shortest_paths --graph &lt;graph_name&gt; --src &lt;src_vid&gt;
  --sink &lt;sink_vid&gt; --k &lt;k&gt; [--ignoredgeweight] [--hidepath]
  [--in &lt;cache_name&gt;]
      </pre>

This analytic computes top-k shortest loopless paths with non-negative edge
weights between a pair of vertices.
It is based on Yen's algorithm, optimized to reduce redundant
computation. _--k_, _--src_ and _--sink_ are required arguments.
When _--ignoreedgeweight_ is specified, bi-directional BFS is used as the base
algorithm for the shortest path computation required by the Yen's algorithm;
otherwise, Dijkstra's algorithm is used.

#### Find path: _analytic_find_path_

    <pre style="border:1px; background-color:#eeeeee; white-space:pre-wrap;
    word-wrap: break-word;">

  analytic_find_path --graph &lt;graph_name&gt; --src &lt;src_vid&gt;
  [--sink &lt;sink_vid&gt;] [--maxnumhops &lt;num_hops&gt;]
  [--label &lt;edge_label&gt;] [--in &lt;cache_name&gt;]
      </pre>

This analytic uses BFS to find a path between a source vertex and a sink
vertex or any other vertex,
with the optional constraints that the max number of hops on the path cannot
exceed the value of _--maxnumhops_
and/or that all edges on the path must have the same label value as specified
by _--label_.

[Back to top](#top)

<a name="multi-user"></a>

## Multi-User Support

gShellSuperMgr is used for the server-side processing of gShell in multi-user
mode. gShellClientMulti is used by the client to communicate with the server.
In addition to the gShell commands described above, there are several
additional commands supported by gShellSuperMgr to manage users.

### Register a user

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "register &lt;username&gt; &lt;password&gt;"
  &lt;username&gt; &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

### Login a user

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "login &lt;username&gt; &lt;password&gt;"
  &lt;username&gt; &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

### Logout a user

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "logout &lt;username&gt;" &lt;username&gt;
  &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

### Check the status a user (active or inactive)

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "check_user &lt;username&gt;" &lt;username&gt;
  &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

### List all registered users and the port number assigned to each for
    communicating with gShell server

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "list_users" admin &lt;server_ip&gt; &lt;socket_port&gt;

</pre>
A port number of 0 means that the user is inactive (logged out).

### Get the number of active users

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "num_users" admin &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

### Terminate gShellSuperMgr

<pre style="border:1px; background-color:#eeeeee">

  ./gShellClientMulti "bye" admin &lt;server_ip&gt; &lt;socket_port&gt;

</pre>

[Back to top](#top)

    </td>
	    <td> </td>
		  </tr>
		  </table>

</body>
</html>
