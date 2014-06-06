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

  * __Example of creating and populating graph__: (full code can be found at examples/generic_graph.cc)    
  
  ```cpp
// start a new graph. if the graph exists, it will be opened.
    graph_type * g = new graph_type("dgraph", "database", ibmppl::PRED_DIRECTED);

    // load vertex csv file. if the vertex already exists, 
    //      its property will be updated (its label won't)
    g->load_csv_vertices("test_vertices.csv",true,",",0,"",2); 
    // load edge csv file. if the src/targ vertex doesn't exist,
    //      it will be added with a given default label.
    g->load_csv_edges("test_edges.csv",true,",",0,1,"EDGE",0,"na");
    
    // if a graph is opened by new, 
    //      it needs to be properly closed by delete. 
    //      Otherwise, some metadata may be dangling.
    delete g;
  `````

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
  
  * __Example of graph queries__: (full code can be found at examples/generic_graph.cc)
  
  ```cpp
cout<<"open graph now\n";
    // open an existing graph.
    g = new graph_type("dgraph", "database", ibmppl::PRED_DIRECTED);

    size_t vid1,vid2,vid3,vid4,vid5;
    // add new vertices and return the id of new vertices. 
    //      if the external id already exists, it will return the id of existing vertex
    // arguments:   <label> <external id>
    vid1 = g->add_vertex("NEW", "new-add-1");
    vid2 = g->add_vertex("NEW", "new-add-2");
    vid3 = g->add_vertex("NEW", "new-add-3");
    vid4 = g->add_vertex("NEW", "new-add-4");
    vid5 = g->add_vertex("NEW", "new-add-5");

    vertex_iterator vit;
    // search vertex by its internal id
    vit = g->find_vertex(vid1);
    // add/set its subproperty
    // arguments:   <subproperty name> <subproperty value>
    if (vit!=g->vertices_end()) vit->set_subproperty("EXTRA_PROP","prop-1");

    // search vertex by its external id
    vit = g->find_vertex("new-add-2");
    if (vit!=g->vertices_end()) vit->set_subproperty("EXTRA_PROP","prop-2");
    
    edge_iterator eit;
    size_t eid;
    // add new edges and return their iterators
    // arguments:   <source vid> <target vid> <label>
    eit = g->add_edge_ref(vid1, vid2, "NEWEDGE"); 
    eit = g->add_edge_ref(vid2, vid3, "NEWEDGE"); 
    eid = eit->id();
    eit = g->add_edge_ref(vid3, vid4, "NEWEDGE"); 
    eit = g->add_edge_ref(vid4, vid5, "NEWEDGE"); 
    eit = g->add_edge_ref(vid5, vid1, "NEWEDGE"); 

    // find edges by its source & target internal vertex id
    std::vector<edge_iterator> edges;
    g->find_edge(vid1, vid2, edges);
    if (!edges.empty()) 
    {
        for (size_t i=0;i<edges.size();i++) 
        {
            edges[i]->set_subproperty("EXTRA_PROP","prop-edge-1");
        }
    }

    // find edge by its source vertex id & edge id
    if (g->find_edge(vid2, eid, eit))
    {
        eit->set_subproperty("EXTRA_PROP","prop-edge-2");
    }

    // find edge by its source&target external vertex id
    g->find_edge("new-add-3", "new-add-4", edges);
    if (!edges.empty()) 
    {
        for (size_t i=0;i<edges.size();i++) 
        {
            edges[i]->set_subproperty("EXTRA_PROP","prop-edge-3");
        }
    }

    delete g;
    cout<<"close graph.\n";
  `````
  
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

  * __Example of vertex/edge/pred_iterator__: (full code can be found at examples/generic_graph.cc)
  
  ```cpp
  cout<<"open graph now\n";
  cout<<"print the whole graph:\n";

  // open an existing graph.
  g = new graph_type("dgraph", "database", ibmppl::PRED_DIRECTED);
    
  // traversing the whole graph by iterating over all vertices
  for (vertex_iterator vit=g->vertices_begin();vit!=g->vertices_end();vit++) 
  {
      // print the internal vertex id 
      cout<<"vid-"<<vit->id()<<": ";
      print_vertex_prop(g,vit);
      cout<<endl;

      // iterating over all outgoing edges of this vertex 
      for (edge_iterator eit=vit->edges_begin();eit!=vit->edges_end();eit++) 
      {
          // print edge source/target vertex (internal id), and edge id
          cout<<"\t["<<eit->source()<<"->"<<eit->target()<<" <eid-"<<eit->id()<<">  ";
          print_edge_prop(g,eit);
          cout<<"]\n";
      }
      cout<<" preds:\t";

      // print predecessors and their corresponding edges' id
      for (pred_iterator pit=vit->preds_begin();pit!=vit->preds_end();pit++) 
      {
          cout<<"["<<pit->vertex_id()<<" <eid-"<<pit->edge_id()<<">]";
      }
      cout<<endl<<endl;
  }
    
  delete g;
  cout<<"close graph.\n";
  `````
  * `property_iterator`
    * iterator pointing to a subproperty of vertex/edge
    * `subproperty_name()`: return the name(key) of current subproperty.
    * `subproperty_value()`: return the value of current subproperty.
    
  * __Example of property_iterator__: (full code can be found at examples/generic_graph.cc)
  
  ```cpp
  void print_vertex_prop(graph_type *g, vertex_iterator& vit)
  {
      // iterating over all subproperties of given vertex
      property_iterator iter = vit->property_begin();
      for (;iter!=vit->property_end();iter++) 
      {
          cout<<"<"<<iter->subproperty_name()<<" : "<<iter->subproperty_value()<<">";
      }
  }
  
  void print_edge_prop(graph_type *g, edge_iterator& eit)
  {
      // iterating over all subproperties of given edge
      property_iterator iter = eit->property_begin();
      for (;iter!=eit->property_end();iter++) 
      {
          cout<<"<"<<iter->subproperty_name()<<" : "<<iter->subproperty_value()<<">";
      }
  }
  `````

<b>For detailed interface specification, refer to [IBM PPL library API] (http://ibmppl.github.io/ibmppl/index.html) </b>
