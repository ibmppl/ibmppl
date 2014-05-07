## Tutorial on Using MultipropertyGraph in IBMPPL

- Define graph type

```bash
   typedef ibmppl::ibm_multiproperty_persistent_graph graph_t;
   typedef ibmppl::ibm_multiproperty_inmemory_graph   memgraph_t;

   typedef graph_t::vertex_iterator vit_t;
   typedef graph_t::edge_iterator   eit_t;
   typedef graph_t::pred_iterator   pred_t;
   typedef graph_t::vertexd_type    vid_t;
   typedef graph_t::edged_type      eid_t;

   typedef memgraph_t::vertex_iterator memvit_t;
   typedef memgraph_t::edge_iterator   memeit_t;
   typedef memgraph_t::pred_iterator   mempred_t;
   typedef memgraph_t::vertexd_type    memvid_t;
   typedef memgraph_t::edged_type      memeid_t;

   typedef int label_t;
````

Hereafter we assume the persistent graph is used, although all APIs are appliable to inmemory graph as well.

- Declare a graph

We provide the storename and the directory for both graphs, since there are some stored meta data for both.

```bash
graph_type g("name", "directory", "directness");    !!! changes for having global properties !!!
memgraph_type g("name", "directory",  "directness");
````

- Add vertices

```bash
   label_t vlabel;
   vid_t vid = g.add_vertex(vlabel);
````
- Add edges

```bash
   vid_t src, targ;
   label_t elabel;
   eid_t eid = g.add_edge(src, targ, elabel);
````
- Find vertices

```bash
   vit_t vit = g.find_vertex(vid);
   vit_t vit = g.find_vertex(pkey, pval);
````
- Find edges

```bash
   vid_t src, targ;
   eit_t eid;
   eit_t eit = g.find_edge(src, eid);  
   eit_t eit = g.find_edge(src, targ);   // need to add!!!
````
- Property management

```bash
   string pkey, pval;
   vit->set_subproperty(pkey, pval);
   eit->set_subproperty(pkey, pval);
   
   string pval = vit->get_subproperty(pkey);
   string pval = eit->get_subproperty(ekey);

   size_t pid = get_vpropertyid(pkey);
   size_t pid = get_epropertyid(pkey);
  
   string pkey = get_vertex_property_name(pid);
   string pkey = get_edge_property_name(pid);
  
   vit->get_int_subproperty(pid);
   vit->get_double_subproperty(pid);
   time_t t = vit->get_time_subproperty(pid);

   int k = get_subpropertytype(pid);
   k = {CSVP_SUBPROPTYPE_STRING, CSVP_SUBPROPTYPE_INT, CSVP_SUBPROPTYPE_DOUBLE, CSVP_SUBPROPTYPE_TIME}

   g.delete_subproperty(pkey);
   g.delete_subproperty(pid);
   
   bool g.has_subproperty(pkey);
````

   Traverse the properties:

```bash
   size_t n = g.get_subproperty_count();
   size_t pid = get_first_subproperty_id();
   size_t pid = get_next_subproperty_id(pid);
````
   

- Traversal
   
```bash
   label_t lid;

   for (vit_t vit=g.vertices_begin(lid); vit!=g.vertices_end(lid); vit++)

   for (eit_t eit=vit.edges_begin(lid); eit!=vit.edges_end(lid); eit++)  // ???
   for (eit_t eit=vit->edges_begin(lid); eit!=vit->edges_end(lid); eit++)  // ???

   for (eit_t eit=vit.preds_begin(lid); eit!=vit.preds_end(lid); eit++)  // ???
````

- Get number of edges for a vertex

```bash
   vit->edges_size(lid);
   vit->preds_size(lid);
````
- Get end vertices of an edge

```bash
   eit->source();   // eit.source()??
   eit->target();
   eit_t eit = eit->id();
````
- Deletion

```bash
   vid_t src, targ;
   g.delete_edge(src, targ);
````    

