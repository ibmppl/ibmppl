# Gstore version 2 design draft #

gstore v2 is the new version of kvstore, the persistent layer of native
store. It consists of a global configuration file and a set of files. We refer
to these files as **tables**, although they can be different from relational
tables. This design aims at improving the performance of the last version, and
optionally incorporte with multiversioning and external properties (similar to
the 2nd, 3rd property bundle) in the first design.

## Global configuration table ##

The graph engine shall choose property data structure to create/load graphs
to/from disk.

|`name` | `value` |
|------|-------|
| vertex_history   |  disabled    |
| num_extra_vertex_property_bundles  | 0   |
| edge_history | disabled |
| num_extra_edge_property_bundles | 0 |
| ... | ... |

`name` and `value` are both strings. This table will be loaded when open a
graph as a key-value hashmap. It is the individual module's responsibility to
interpret the value.

## Vertex record ##

| `flag` | `inEdge` `cnt` | `outEdge` `cnt`| `property` `cnt` | `history` | `property2` | ... |
|--------|----------|----------|------------|-----------|-------------|-----|
|  ...   |  ...    | ... | ... | ... | ... | ... |


Each row in this table starts for a  vertex. Except the first column `flag`,
others are all in format of a pointer. By pointer, we mean an offset of
another file, where the details can be found. This table should be mmapped
into memory whenever is possible.

- `flag`: a `uint8` to bitmap flags such as **deleted**, **locked**, etc.
- `inEdge`: a pointer (offset) to an entry in the edge list table to find the
  incoming edge list
- `outEdge`: a pointer to an entry in the edge list table to find the outgoing
  edge list
- `property`: a pointer to an entry in the property bundle table
- `history`: a pointer to an entry in the history (versioning) table
- `property*`: a pointer to an entry in the additional property bundle table
- `cnt`: the number of elements filled in the last buffer of the edge
  list/property buffer. This helps to determine where we can append new
  edges/property. Since the size of a single buffer is not large typically
  (say, 256bytes for the kvstore), we can use `uint16`.

Therefore, if there is only a single property bundle (encoded multiple
properties) for a vertex, the vertex record size is:
```bash
   39 bytes = uint8 + size_t(uint64) * 4 + uint16 * 3
```
For a graph with 120M vertices, the table size is about `39B * 120M
= 4.7GB`. This seems reasonable for most servers. 

## Edge lists ##

<u>[OPEN QUESTION: shall we have a single edge list table, or two - one for incoming edges and one for outgoing edges?]</u>

The edge list table has a header and a fixed length buffer, storing a list of
edge elements.

- `header`: is used for chain multiple buffers together. The buffer size must
be aligned with the element of the edge list. For now, we only have `prev` in
the header as the pointer to the previous edge list buffer


- `edge_list_buffer`: The element is *configured* according to the global
configuration table. Typically, it is a tuple of three subelements: `<eid,
vid, lid>`, standing for the edge ID, the vertex ID, and the label ID. The
`vid` is the `src_vid` for incoming edges and `targ_vid` for outgoing
edges. The `eid` is the offset of the edge in the edge record table. According
to the configuration, `lid` may be skiped. In this case, the graph engine
shall handle it by generating a fake identical label for all edges. A special
`eid` can be used for indicating the element is invalide (e.g. deleted).

| `prev` | `edge_list_buffer` |
|--------|---------------------|
| ... | ... |

Note that in **insert** mode, the edge list of a vertex forms a reversed chain
buffer. The vertex record always points the last record; while each record
points to the earlier one. The reason is that the order of the edge tuples
does not matter. They will be reordered by the label id `lid` after loading
into memory. Therefore, when inserting new edges, it will only append data to
a buffer or create new buffers. No need to touch earlier data.

```bash
                    ---------------------------------
                    prev | <eid,vid,lid>, <>, ..., <>
                    ---------------------------------
                      ^
	                  |
vertex record:      ---------------------------------
(in/outEdge) ======>prev | <eid,vid,label>, <>, ... 
                    ---------------------------------
			                                  ^		
(cnt) ----------------------------------------|
```


## Vertex history table ##

This conforms with the vertex record table. Note the entry `history` will
point to the earlier record, if any.

## Vertex property table ##

Vertex property table is pretty similiar to the edge list table, where the
property is store in a chained buffer, but we only
point to the last buffer in the vertex record table. The vertex record table
also tells us where the end of the valid data in the last buffer, so that we
can easily pull out correct information. Note that for the property loader in
the graph engine, it should read the buffer in reversed
order. [Will this be an issue for the parsers??]

```bash
                 ---------------------------------
                 prev | property_buffer
                 ---------------------------------
                   ^
	               |
vertex record:   ---------------------------------
(property)======>prev | property_buffer ...
                 ---------------------------------
			                           ^		
(cnt) ---------------------------------|

```

## Edge record ##

Edge record is a subset of the 

| `flag` | `property` `cnt` | `history` | `property2` | ... |
|--------|----------|----------|------------|-----------|
|  ...   |  ...    | ... | ... | ... |

## Edge property table ##

This conforms with the vertex property table.

## Edge history table ##

This conforms with the vertex history table.


----------------------------------

## API proposal ##

<!--
// data structures: vertex list, inEdge list, outEdge list, edges, properties,
history_optional
  // create a store

  // configure a store

  // add vertex, edge or property to a store
    // addVertex key is offset in the vertex table, if key=-1, then the offset
    of new added vertex is returned
	  // You need to add a Vertex before you add edges from/to the vertex
	    int addVertex     (size_t &vid);
		  // (eid, vid, lid) edges include vid and label of a bunch of edges,
    label may be 4 bytes int
	  int addOutEdge     (size_t vid, size_t &eid, size_t vid2, size_t lable,
    bool newEdge=true);
	  // just byte copy, no guanrantee of the validity of the eids
	    int addOutEdges    (size_t vid, byte_type *edges, size_t edgeSize,
    bool newEdge=true);
	  int addInEdge      (size_t vid, size_t &eid, size_t vid2, size_t lable,
    bool newEdge=false);
	  // just byte copy, no guanrantee of the validity of the eids
	    int addInEdges     (size_t vid, byte_type *edges, size_t edgeSize,
    bool newEdge=false);

  int addVertexProperties (size_t vid, size_t propertyBundleId, byte_type
  *properties, size_t propSize);
    int addEdgeProperties   (size_t eid, size_t propertyBundleId, byte_type
  *properties, size_t propSize);

  // update
    // update can be remove first, then add later

  // delete
  // also delete all the edges, properties of it
    int deleteOutEdge (size_t vid, size_t eid, bool deleteEdgeRecord=true,
  bool reclaimSpace);
    int deleteInEdige (size_t vid, size_t eid, bool
  deleteEdgeRecord=false,bool reclaimSpace);
    int deleteVertexProperty (size_t vid, bool reclaimSpace);
	  int deleteEdgeProperty   (size_t eid, bool reclaimSpace);

  // query vertex, edge or property from a store
    int getVertex   (size_t vid, size_t &inEdgeCnt, size_t &outEdgeCnt,
    size_t* propertySize);
	  int getOutEdges (size_t vid, byte_type* edges, size_t edgesSize);
	    int getInEdges  (size_t vid, byte_type* edges, size_t edgesSize);
		  int getVertexProperty (size_t vid, size_t propBundle_id, byte_type*
    prop);
	  int getEdgeProperty   (size_t eid, size_t propBundle_id, byte_type*
    prop);

  // filtering

  // retrieve information of a store

  // util
    // reclaim all the deleted space
	  // level=1, garbageCollection in  vertex list
	    // level=2, plus in edge list
		  // level=3, plus in edge records
		    // level=4, plus in properties
			  int garbageCollection (size_t level);int deleteVertex  (size_t vid, bool reclaimSpace);

-->


=======================================================


## add vertex, edge or property to a store ##

addVertex

`key` is offset in the vertex table, if key=-1, then the offset of new added vertex is returned. You need to add a Vertex before you add edges from/to the vertex

```bash
	int addVertex (size_t &vid, byte_type *inEdgeList=NULL, byte_type *outEdgeList=NULL, vector<byte_type*> *props=NULL);
```

 `(eid, vid, lid)` edges include vid and label of a bunch of edges, label may be 4 bytes int

```bash
    int addOutEdge     (size_t vid, size_t &eid, size_t vid2, size_t lable, xsbool newEdge=true);
```

just byte copy, no guanrantee of the validity of the `eids`

```bash
    int addOutEdges    (size_t vid, byte_type *edges, size_t edgeSize, bool newEdge=true);
    int addInEdge      (size_t vid, size_t &eid, size_t vid2, size_t lable, bool newEdge=false);
```

just byte copy, no guanrantee of the validity of the `eids`

```bash
	int addInEdges     (size_t vid, byte_type *edges, size_t edgeSize, bool newEdge=false);
	int addEdgeRecords (size_t offset, byte_type *edges, size_t edgeSize);
    int addVertexProperties (size_t vid, size_t propertyBundleId, byte_type *properties, size_t propSize);
    int addEdgeProperties   (size_t eid, size_t propertyBundleId, byte_type *properties, size_t propSize);
```


### update ###

update can be remove first, then add later

### delete ###

also delete all the edges, properties of it

```bash
    int deleteOutEdge (size_t vid, size_t eid, bool deleteEdgeRecord=true, bool reclaimSpace);
    int deleteInEdige (size_t vid, size_t eid, bool deleteEdgeRecord=false,bool reclaimSpace);
    int deleteVertexProperty (size_t vid, bool reclaimSpace);
	int deleteEdgeProperty   (size_t eid, bool reclaimSpace);
```

query vertex, edge or property from a store

```bash
    int getVertex   (size_t vid, size_t &inEdgeCnt, size_t &outEdgeCnt, size_t* propertySize);
	int getOutEdges (size_t vid, byte_type* edges, size_t edgesSize);
    int getInEdges  (size_t vid, byte_type* edges, size_t edgesSize);
	int getVertexProperty (size_t vid, size_t propBundle_id, byte_type* prop);
	int getEdgeProperty   (size_t eid, size_t propBundle_id, byte_type* prop);
```	

### filtering ###

retrieve information of a store until reclaim all the deleted space

- level=1, garbageCollection in  vertex list
- level=2, plus in edge list
- level=3, plus in edge records
- level=4, plus in properties

```bash
	int garbageCollection (size_t level);

    graphStore_type (string store_name);
    virtual ~graphStore_type(){}
```	

Configure a store

```bash
    (string name, string value) { _props.insert (name, value); }
    string getConfig  (string name)               {return _props.at(name); }
```	

```bash
    void importConfig (string fileName);
    void exportConfig (string fileName);
```

create a store when store files do not exist or open a store when files exist

```bash
    void createStore ();
	void importStore ();
```	

### close ###

```bash
    void closeStore ();
	void setConfigint deleteVertex  (size_t vid, bool reclaimSpace);
```
