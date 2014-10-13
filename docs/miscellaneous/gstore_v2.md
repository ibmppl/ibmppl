# Gstore version 2 design draft #

gstore v2 is the new version of kvstore, the persistent layer of native
store. It consists of a global configuration file and a set of files. We refer
to these files as **tables**, although they can be different from relational
tables. This design aims at improving the performance of the last version, and
optionally incorporte with multiversioning and external properties (similar to
the 2nd, 3rd property bundle) in the first design.

## Global configuration ##

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
another file, where the details can be found.

- `flag`: a `uint8` to bitmap flags such as **deleted**, **locked**, etc.
- `inEdge`: a pointer (offset) to an entry in the edge list table to find the incoming edge list 
- `outEdge`: a pointer to an entry in the edge list table to find the outgoing edge list
- `property`: a pointer to an entry in the property table
 
