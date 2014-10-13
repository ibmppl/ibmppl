# Gstore version 2 design draft #

gstore v2 is the new version of kvstore, the persistent layer of native
store. It consists of a global configuration file and a set of files. We refer
to these files as **tables**, although they can be different from relational
tables. This design aims at improving the performance of the last version, and
optionally incorporte with multiversioning and external properties (similar to
the 2nd, 3rd property bundle) in the first design.

## Global configuration table ##

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


