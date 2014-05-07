### Instructions on using Native Graph Store

gShell provides REST-like APIs for langauge-free operations on System G Native Store. Please refer to the gShell main page for the installation and detailed usage of gShell. This document focuses on the REST-like APIs for gShell.

<b> 1. Installation </b>

gShell REST-APIs installation is similar to gShell installation. It consists a perl CGI code (nsREST.pl), a gShell Client (nvStoreClient.c) and a gShell Server (nvStore.cpp) that speaks to ibmppl and graph kv store in System G Native Store. The perl code basically wraps up the gShell commands as REST-like APIs.

<b> 2. Configuration </b>

gShell server is invoked for supporting REST mode as follows:

```bash
    ./nvStore server [socket_port]
```

The client code and the perl CGI code (nvStoreClient and nsREST.pl) must be placed in some directory where CGI is enabled. In the following description, we assume it is: http://127.0.0.1/cgi2/.

<b> 3. REST-like APIs</b>	
The commonly used commands in gShell include:

- Create a store. Assuming we want to create a graph store called "<store_name>", and we want use it to store an undirected graph. Note that a graph is not necessarily to be connected in gShell; that is, a graph store can maintain a set of small graphs, but all of them must be of the same type (directed, undirected, or pred_directed). The command for creating such a store is:

```bash
	http://127.0.0.1/cgi2/nsREST.pl?cmd=create&storename=<store_name>&graphtype=<type>
```

- To close a store, we use "<store_name> close". It remove the store from memory, so that we have more memory to process other stores. So, the memory is release. It is suggested to issue such commands time by time to make the memory free. Note that close_all is not supported in API mode.

```bash
	http://127.0.0.1/cgi2/nsREST.pl?cmd=close&storename=<store_name>
```
 
- List all stores and their types. This command will list all existing stores (opened or not opened) and their respective graph type (directed, undirected, pred_directed). Note that this command will not load any store if they are not opened already. 

```bash
        http://127.0.0.1/cgi2/nsREST.pl?cmd=list_all
```

- Erase a store from the disk. This is a permanent deletion and can not be recovered. So, this command should be used in cautious. 

```bash
        http://127.0.0.1/cgi2/nsREST.pl?cmd=delete&storename=<store_name>
```

- Now, we have <store_name> as an empty graph. A easy way to populate the store is to convert a file, say .csv files or edge list, to the edge store. In the following example, we assume that we have a edge list in csv format called <csv_file>, where each line in the fileconsists of <source node> <target node> <edge weight>. User must indicate that the source and target nodes are given by the <colID_src> and <colID_targ> columns, respectively. The data in the rest columns are treated as the properties on this edge. Note that this command must follow a store name, since gShell can concurrently operate multiple graph stores. If the first row of the .csv file is the header, then users must specify "has_header". We can use comma, tab or blank space to separate columns in the .csv file. The separator is specified by [separators]. If a string contains these separator characters. 

```bash
	under construction
         <store_name> load_csv_edges <csv_file> <colID_src> <colID_targ> [has_header|no_header] [separators]
```         

- Note that in the above edge list file (or .csv file)  we can only have edge properties. In order to create a graph with both edge and vertex properties, we need and additional .csv file. We can run the above operation first to build the graph with edge properties. Then we can read a vertex file to load vertex properties. In the following example, the <colID_vtx>-th column in the vertex file gives the ID of a vertex and the rest columns give the properties of the vertex as a vector of strings. 

```bash
	under construction
         <store_name> load_csv_vertices <csv_file> <colID_vtx> [has_header|no_header]  [separators]
```

- gShell supports interactive graph updates. Here are some examples to add/update vertices/edges. The instruction line also starts with the store name to identify which store to work on, which is followed by the command. The first argument for add_vertex is the vertex ID, and the rest are the vertex properties as a vector of strings. We actually store the vertex ID as the first property. We can update the properties using update_vertex and/or update_edge. In the following example, then "John" is the ID of the vertex and the rest are all properties, separated by blank spaces. Quotes string can include spaces or other characters. If edge (2nd example), the next two words are the source and target vertices and the rest are properties. The number of properties for vertices and edges are arbitrary (0 to 2^64).

```bash
	http://127.0.0.1/cgi2/nsREST.pl?cmd=add_vertex&storename=<storename>&vertex_id=<vertex_id>&property_list=p1%20p2%p3
	http://127.0.0.1/cgi2/nsREST.pl?cmd=update_vertex&storename=<storename>&vertex_id=<vertex_id>&property_list=p1%20p2%p3
	http://127.0.0.1/cgi2/nsREST.pl?cmd=add_edge&storename=<storename>&src_vid=<source>&targ_vid=<target>&property_list=p1%20p2%20p3
	http://127.0.0.1/cgi2/nsREST.pl?cmd=update_edge&storename=<storename>&src_vid=<source>&targ_vid=<target>&property_list=p1%20p2%20p3
```
- The query of a vertex or edge gives all the properties (including the adjacent edges for a vertex). We use the source vertex ID plus the target vertex ID to identify an edge. In the following example, we query the properties, adjacent edges of vertex John and then query the properties of edge (Mary, John).

```bash
         !!! did not pass my test!!! <store_name> query_vertex  <vertex_id>
         !!! did not pass my test!!! <store_name> query_edge    <src_vtx> <targ_vtx>
```

- The deletion is straightforward. We just delete the vertex or edge by giving the ID or the source and target IDs. 

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=delete_vertex&vertex_id=<vertex_id>
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=delete_edge&src_vid=<source>&targ_vid=<target>
```		   

- To get the number of edges and vetices in a graph, we use the following commands.

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=get_num_vertices
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=get_num_edges
```
- To get the number of neighbors of a vertex

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=get_num_neighbors&vertex_id=<vertex_id>
```

- To query all neighbors of a vertex, we use the following command. We just need to provide a vertex ID. 

```bash
        http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=query_neighbors&vertex_id=<vertex_id>
```

- Filter vertices to only output those with the i-th property equal to val

```bash
        http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=filter_vertices&prop_idx=<index>&prop_val=<value>
```

- Find the vertex with the maximum node degree. If the condition i and val are given, it finds the vertex only from those satisfying the condition, i.e., the i-th property of the vertex is equal to val. It also finds the vertices with the top #n number of degrees. 

```bash
        http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=find_vertex_max_degree
```

- Find n vertices randomly from a graph. This command is for users to get some vertices, so that they can use such vertices as start points for certain analytics. <n> is a number, say 10.

```bash
        http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=find_random_vertices&n=<#n>
```
- Find n edgess (nearly) randomly from a graph. This command is for users to get some edges, so that they can use such vertices as start points for certain analytics. <n> is a number, say 10.

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=find_random_edges&n=<#n>
```

- To query the property keys of the vertices and edges, we use the following commands. If there is no such keys (i.e., the data was imported with arguemnt "no_header"), a notice is shown to tell that there is no property keys.

```bash
        http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=query_vpropkeys
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=query_epropkeys
```

<b> 4. Plug-In Analytics </b>

- A user controled Breadth First Search (BFS) can be invoked by the following commands. <root> is an arbitrary vertex in the graph stored in <store_name>, and #hops shows the maximum allowed BFS levels. <max_breadth_per_level> gives the maximum number of vertices to traverse at each BFS level. This is for visualization purpose, where we do not want to visualize all the edges for dense vertices. [json|plain] defines if the output format should be in JSON or simply in plain text.

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=bfs_visual&root=<vertex_id>&hops=<#hops>&max_breadth=<#max_breadth>
```

- It is possible to run some analytic routines using the data store. Any graph analytic applications that are developed using System G middleware APIs shall be easily plugged into the shell. In this command, we use a collaborative filter code. Collaborative filter is widely used in recommandation systems and has many alternatives. In this version, it takes a bipartite graph G((X, Y), E) as the input, and finds <i>relevant</i> vertices to a user specificed vertex, say x∈X. The most relevant vertex is z = argmax |neighbors(x) ^ neighbors(z)| for any z∈X.  The analytics queries a vertex called <vertex_id> in the graph store and performs BFS for <#hops> levels. It computes the number of paths from the root vertex to any leaves and rank these leaves accordingly in descending order. The top <#ranks> vertices are returned. The result can be formatted into json format if the optional argument [json] is specified.

```bash
       http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=colFilter&vertex_id=<vertex_id>&hops#=<n>&ranks=5
```		  

- There is a relevant command called centroid visualization for recommandation (centroid_visual). The first argument <vertex_id> for this command is also the queried vertex ID, but it performs a 2 hops colFilter and got the top <#rank1> nodes, and then for each of them perform 2 hops again and get the top 10 nodes. The results are of the top #rank from the 1st colFilter and the top <#rank2> of the remaining colFilter are aggregated to return. The result can be formatted into json if the optional argument is specified.

```bash
	 http://127.0.0.1/cgi2/nsREST.pl?storename=<store_name>&cmd=centroid_visual&vertex_id=Y077571E64061O86&rank1=<rank1>&rank1=<rank2>
```
- We have a plug-in analytic call pageRank, which performs persistent page rank in a pred_directed graph. By persistent page rank, we mean that the importance of each vertex is stored in each iteration. Thus, we can incrementally perform page rank at any time, or after any changes to the graph. Given a directed graph G(V, E), pageRank works by counting the number and quality of edges to a vertex to determine a rough estimate of how important the vertex is in the graph. The quality is iteratively computed by: PR(v_i) = (1-d)/N + d ∑<sub>{v_j∈ neighbors(v_i)}</sub> PR(v_j)/L(v_j), where N=|V|; d is the damping factor and L(v_j) is the number of outgoing edges of vertex v_j. The underlying assumption is that more important websites are likely to receive more links from other websites. The arguments for the command are the damping factor, the quadratic error bound and the initialization control. The damping factor and quadratic error are explained in wiki. By specifying "restart", we re-initialize the importance of each vertex; otherwise, if we omit it, we use the current stored values for ranking. Note that due to a lot of string to number conversions, the performance might be adversely impact. For performing high-performance page rank, please choose our in-memory page ranking subroutine in "apps/pagerank/" directory.

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=pageRank&dumpling_factor=0.2&quadratic_factor=0.5
```

- ConnectedComponent, which finds all connected components in a graph. It takes an undirected graph as input and outputs in json format the following information: 1) a list of all the nodes in the graph with the component label for each node, 2) a list of all the edges in the graph with the component label for each edge, 3) a list of connected component with the labels of nodes contained in each component. To run:

```bash
         http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=connectedComponent
```

- kCore, which finds the K-core of a graph, where K is a parameter specified by the user. A K-core of a graph G is a maximal connected subgraph of G in which all nodes have degree at least K. It takes an undirected graph and K as input and outputs in json format the following information: 1) a list of nodes in the K-core, 2) a list of edges in the K-core. To run:

```bash
         http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=kCore&k=2
```

- ClusteringCoefficient, which computes the local clustering coefficient of each node in an undirected or directed graph. Let N be the neighborhood of a node (immediately connected neighbors), let n be |N|, i.e. size of N. The local clustering coefficient C of this node is the number of links (edges) between the nodes within N divided by n*(n-1) for a directed graph or n*(n-1)/2 for an undirected graph. It takes a graph (undirected or directed) as input and outputs in json format the following information: 1) a list of all the nodes in the graph with the local clustering coefficient value for each node, 2) a list of all the edges in the graph. To run:

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=clusteringCoefficient
```

- TriangleCount, which computes the triangle count on each node of an undirected or directed graph. For a directed graph, it counts the total number of in-, out-, through-, and cycle-triangles separately. It takes a graph (undirected or directed) as input and outputs in json format the following information: 1) a list of triangles with type and count information, 2) a list of all the nodes in the graph with the triangle count(s) for each node, 3) a list of edges that belong to the triangles. To run:

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=triangleCount
```

- ShortestPaths, which computes the shortest paths from a given node to any other node in an undirected or directed graph, and two closeness centrality measures: 1) using the original formula, which is C(i)=1/(sum(shortest_distance(i, j)) for all j != i, 2) using Opsahl 2010 formula, which is C(i) = sum(1/shortest_distance(i, j)) for all j != i. It takes a graph (undirected or directed, with optional weight on each edge specified in the edge list data file) and the label of the target node as input and outputs in json format the following information: 1) a list of nodes with shortest distance value, number of shortest paths, and shortest paths (number of hops, sequence of nodes on each path) information from the target node to each of these nodes, 2) the closeness centrality measures of the target node, 3) a list of all the edges in the graph. To run:

```bash
	http://127.0.0.1/cgi2/nsREST.pl?storename=kv11&cmd=ShortestPaths&targ_vid
```


<b> Note </b>

More commands and plugin analytics are addition to gShell. Please contact Yinglong Xia for further information.



