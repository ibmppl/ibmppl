##IBMPPL Programming Guide

###Generic Graph

Generic graph is a high level interface on top of IBMPPL native graph store. It provides graph operations with strict persistence support. Generic graph allows users to easily add vertex/edge, load csv files, and traverse graph. The details are explained as follows.

- Define graph type and related iterators
  * Before declaring a graph and operating on it, users should first define graph_type and corresponding iterators as follows. 
  ```cpp
  // define graph type as generic graph
  typedef ibmppl::ibm_generic_graph       graph_type;
  // define iterators
  typedef graph_type::vertex_iterator     vertex_iterator;
  typedef graph_type::edge_iterator       edge_iterator;
  typedef graph_type::pred_iterator       pred_iterator;
  typedef graph_type::property_iterator   property_iterator;
  // define types of vertex/edge id
  typedef graph_type::vertexd_type        vertexd_type;
  typedef graph_type::edged_type          edged_type;
  ````

- Create/open graph
  
  * `graph_type(string graphname, string path, DIRECTNESS direct=ibmppl::PRED_DIRECTED, UINT64 max_memsize=4294967295)`
  * Create a new graph by declaring an instance of graph_type. If the graph already exists, it will just be opened. If using `new` to generate the instance, `delete` should be properly called to avoid dangling meta data.
  * __arguments__: `graphname`: graph name. `path`: path of the graph native store. `direct`: (optional) directness of the graph. It can be ibmppl::PRED_DIRECTED|DIRECTED|UNDIRECTED.  `max_mem_size`: (optional) maximum allowed memory size in bytes. Default value is 4GB. 


- Update graph

  * `vertexd_type add_vertex(string label, string external_id)`
    * add a new vertex into graph using given label and external id
    * __return__: vertex id of the new added vertex
    * __arguments__:  `label`: vertex label.  `external_id`: (optional) a globally unique string id for vertex

  * `edge_iterator add_edge_ref(vertexd_type source, vertexd_type target, string label)`
    * add a new edge into graph and return the iterator of it
    * __return__: iterator of the new edge
    * __arguments__: `source`: source vertex id.  `target`: target vertex id. `label`: edge label
  
- Populate graph (load CSV files)

  * `bool load_csv_vertices(string filename, bool has_header, string separators, size_t keypos, string global_label, size_t labelpos)`
    * load vertices from a csv file into graph. If the vertex already exists in graph, its property will be updated.
    * __return__: success or not
    * __arguments__: `filename`: csv file name. `has_header`: if csv file has header. `separators`: separators used in the csv file.  `keypos`: column # of external vertex id (starting from 0).  `global_label`: if not empty, set all vertices to this label. `labelpos`: if global_label is empty, get label from csv file according to this column #.
  
  * `bool load_csv_edges(string filename, bool has_header, string separators,                                      
                       size_t srcpos, size_t targpos,                                          
                       string global_label, size_t labelpos,                                   
                       string default_vertex_label="na")`
    * load edges from a csv file into graph. If edge source/target vertex doesn't exist, it will be added into graph using the default_vertex_label.
    * __return__: success or not
    * __arguments__: `filename`: csv file name. `has_header`: if csv file has header. `separators`: separators used in the csv file. `srcpos`&`targpos`: column # of external source/target vertex id (starting from 0).  `global_label`: if not empty, set all edges to this label. `labelpos`: if global_label is empty, get label from csv file according to this column #.  `default_vertex_label`: label of newly added vertex
    
- Query graph
  * `vertex_iterator find_vertex(vertexd_type vertex_id)`
    * find vertex by vertex id
    * __return__: a vertex iterator to this vertex. If cannot find it, returns an iterator to *vertices_end()*
    * __arguments__: `vertex_id`: vertex id
    
  * `vertex_iterator find_vertex(string external_vertex_id)`
    * find vertex by vertex id
    * __return__: a vertex iterator to this vertex. If cannot find it, returns an iterator to *vertices_end()*
    * __arguments__: `external_vertex_id`: a string external vertex id (set when adding vertex)
  
  * `void find_edge(string source, string target, std::vector<edge_iterator>& ret)`
    * find edges between given source/target vertex.
    * __return__: none
    * __argument__: `source`&`target`: string external id of source/target vertex.  `ret`: (reference) a vector of iterators of found edges. If cannot find it, the vector will be empty

  * `void find_edge(vertexd_type source, vertexd_type target, std::vector<edge_iterator>& ret)`
    * same as above except for using vertex id directly
    
  * `bool find_edge(vertexd_type source, edged_type eid, edge_iterator& ret)`
    * find edge with given source vertex id and edge id.
    * __return__: find it or not
    * __arguments__: `source`: source vertex id.  `eid`: edge id. `ret`: (reference) iterator of found edge
  
- Graph iterators
  * `vertex_iterator`
    * iterator pointing to a vertex. Through calling its member functions, users can get vertex id, vertex property, outgoing edges, and predecessors.
    * `id()`: return vertex id.
    * `get_external_id()`: return a string external id. exception may happen if external id doesn't exist.
    * `get_label()`: return vertex label.
    * `edges_size()`: return num of outgoing edges.
    * `edges_begin()`: return an *edge_iterator* pointing to the first edge of this vertex.
    * `edges_end()`: return an *edge_iterator* referring to past-the-end edge.
    * `preds_size()`: return num of predecessors.
    * `preds_begin()`: return a *pred_iterator* pointing to the first predecessor of this vertex.
    * `preds_end()`: return a *pred_iterator* referring to past-the-end predecessor.
    * `property_begin()`: return a *property_iterator* pointing to the first subproperty of this vertex.
    * `property_end()`: return a *property_iterator* referring to past-the-end subproperty.
    * `get_subproperty(const string& pname)`: return subproperty value of given name(key).
    * `set_subproperty(const string& pname, const string& pvalue)`: add/update subproperty with given name and value

  * `edge_iterator`
    * iterator pointing to an edge. Through calling its member functions, users can get edge id, edge source/target vertex id, and edge property.
    * `id()`: return edge id.
    * `source()`: return source vertex id.
    * `target()`: return target vertex id.
    * `get_label()`: return edge label.
    * `property_begin()`: return a *property_iterator* pointing to the first subproperty of this edge.
    * `property_end()`: return a *property_iterator* referring to past-the-end subproperty.
    * `get_subproperty(const string& pname)`: return subproperty value of given name(key).
    * `set_subproperty(const string& pname, const string& pvalue)`: add/update subproperty with given name and value

  * `pred_iterator`
    * iterator pointing to a predecessor.
    * `vertex_id()`: return predecessor vertex id.
    * `edge_id()`: return id of the corresponding edge.
  
  * `property_iterator`
    * iterator pointing to a subproperty of vertex/edge
    * `subproperty_name()`: return the name(key) of current subproperty.
    * `subproperty_value()`: return the value of current subproperty.

<b>For detailed interface specification, refer to [IBM PPL library API] (http://ibmppl.github.io/ibmppl/index.html) </b>
