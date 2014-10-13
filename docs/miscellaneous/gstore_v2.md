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
| k0   | v0    |
| ...  | ...   |

`name` and `value` are both strings. This table will be loaded when open a
graph as a key-value hashmap. It is the individual module's responsibility to
interpret the value.

## Vertex record ##

| `flag` | `inEdge` | `outEdge`| `property` | `history` | `property2` | ... |
|--------|----------|----------|------------|-----------|-------------|-----|
|  ...   |  ...    | ... | ... | ... | ... | ... |


Each row in this table starts for a  vertex. Except the first column `flag`,
others are all in format of a pointer. By pointer, we mean an offset of
another file, where the details can be found. This table should be mmapped
into memory whenever is possible.

- `flag`: a `uint8` to bitmap flags such as **deleted**, **locked**, etc.
- `inEdge`: a pointer (offset) to an entry in the edge list table to find the incoming edge list 
- `outEdge`: a pointer to an entry in the edge list table to find the outgoing edge list
- `property`: a pointer to an entry in the property table
- `history`: a pointer to an entry in the history (versioning) table
- `property*`: a pointer to an entry in the additional property table

## Edge lists ##

<u>[OPEN QUESTION: shall we have a single edge list table, or two - one for incoming edges and one for outgoing edges?]</u>

The edge list table has a header and a fixed length buffer, storing a list of
edge elements.

- `header`: is used for chain multiple buffers together. The
buffer size must be aligned with the element of the edge list.
  - `prev`: pointer to the previous edge list buffer
  - `cnt` : number of tuples in this buffer

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
    prev | <eid,vid,lid>, <>, ...
    ---------------------------------
      ^
	  |
    ---------------------------------
 -->prev | <eid,vid,label>, <>, ... | 
    ---------------------------------
```

## Vertex history table ##

This conforms with the vertex record table. Note the entry `history` will
point to the earlier record, if any.

## Property table ##

This is the same chain buffer as it is used in the current kvstore. No update
is provided for now.

## Edge record ##

In most cases, the only reason for accessing an edge recard is to access the
edge property. Therefore, it makes sense to store the property directly along
with the edge record, so that we can save an additional jump.

Edge record is like a 

| `flag` | `property` | `history` | `property2` | ... |
|--------|----------|----------|------------|-----------|
|  ...   |  ...    | ... | ... | ... |


