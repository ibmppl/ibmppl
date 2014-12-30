## Persistency-Amenable String-Integer Mapping ##

This is the implementation of a persistency-amenable mapping from a
key (typically a string) to a non-negative integer, both provided
by users. Unlike the ordinary hashmap, the proposed design is
suitable for mapping an external key into an internal ID, where the
ID is contiguously distributed from 0 to a limited integer N. Simply speaking, the keymap works as:

```bash 
  M.insert(key, ID); ID = M.find(key); M.erase(key); ... 
```
 
The key is treated as a byte buffer, so it is not necesssarily zero
terminated. We accept stl::string as input keys, which are not zero
terminated as well.
 
The integer is from 0 to N, where N is theoretically up to
numeric_limits<INT64>::max()-1. Since a contiguous buffer from 0 to
N will be created, it is suggested to keep N as small as possible.
 
The implementation comes with a native garbage collection for
re-using the slots of deleted keys/IDs. The collected slots are
also persisted when persisting the mapping.
 
The design is persistency-amenable, since it organized all data in
a few arrays (vectors). Except one of the arrays storing the keys,
the others have equal element size within an array. Therefore, the
loading/saving and searching is highly efficient. 
 
The hashing is based on the FNV64a algorithm, which is featured by
its highly efficient computing. The mapping is organized as a
three-level vectors. Ideally, the ID is found at level 1
(L1). Dependent on L1 capacity, the keys with conflicts in L1 are
chained at L2, where the full hash code is stored. Imperically, the
chain is of very short length, which makes the search highly
efficient. If the conflict occurs in L2 too, a chain is built in
L3, where the original key is used for solving the conflict. In
most cases, the ID is found at L2, with very limited comparisons of
hash codes. A iterator is provided for convenience. 

### L1 ###
           -----------
           | ID/Index|
           -----------
           |         |
           -----------
hc%N --->  |         |
           -----------
		   |         |
