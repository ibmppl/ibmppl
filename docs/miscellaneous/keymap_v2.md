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

Given a key (a byte buffer, or a stl::string) and an ID (non-negative
integer), we convert it into a hash code. In our current implementation, we
use FNV_a64 algorithm to convert a key into a 64bit unsigned code. In the
first list (L1), we modulo the hash code by N, the size of the list, and use
the result as the offset in L1 for storing the corresponding ID.

ID and Index can be identified by checking its MSB (most significant bit).

```
hc = fnv_hash(key)
           L1:
           ------------ 
           | ID/Index | 
           ------------
           |          | 
           ------------ 
hc%N --->  |          | 
           ------------
		   |          |
```

### L2 ###

If L1 gives an index instead of an ID, we proceed to L2:

```
           L2:
		   ------------------------------
           | Hashcode | ID/Index | Next |
		   ------------------------------
L1Index--->|          |          |   2  |  -----
		   ------------------------------      |
		   |          |          |      |      |
		   ------------------------------      |
		   |          |          |      | <-----
```

### L3 ###

L3 solves all conflicts that L2 can not help. It saves chains of IDs and
pointers to d. When search in a chain, it reads an ID and pulls out the
corresponding string from a different list (V).

```
          L3:
		  ---------------
		  |  ID  | Next |
		  ---------------
		  |      |      |<----
		  ---------------    |
L2Index-->|      |      |-----
		  ---------------
		  |      |      |
```

### V ###

V is a vector of stl::string, where the k-th element stores the key of which
the corresponding ID is k. If a slot has not key, it is marked as
`invalid_str`.

### keymap class ###

```cpp
class keymap_t {                                                                                                                                       
private:                                                                                                                                               
    _L1_t L1;                                                                                                                                          
    _L2_t L2;                                                                                                                                          
    _L3_t L3;                                                                                                                                          
    _V_t  V;                                                                                                                                           
    _data_t           invalid_data;                                                                                                                    
    _index_t          invalid_index;                                                                                                                   
    string            invalid_str;                                                                                                                     
                                                                                                                                                       
public:                                                                                                                                                
    keymap_t(size_t num_bucket);      ///< constructor of keymap                                                                                       
                                                                                                                                                       
    size_t size() { return V.size(); }     ///< return the number of keys                                                                              
    const string & at(_index_t i) { return V.at(i); }          /// return the key of ID i (not confused as the i'th key)                               
    const string& operator[](_index_t i) { return V.at(i); }   /// the same as .at() method                                                            
                                                                                                                                                       
    void insert(const string &str, _data_t id);  ///< insert a key with corresponding ID                                                               
    bool erase(const string &str);               ///< delete a key                                                                                     
    _data_t find(const string &str);             ///< find the ID given a key                                                                          
                                                                                                                                                       
    void load(const string &filename);     ///< load the map from disk                                                                                 
    void save(const string &filename);     ///< save the map to disk                                                                                   
                                                                                                                                                       
    void print();                          ///< print the map (for debugging)                                                                          
    void statistics();                     ///< print the statistics (e.g. hit rates)                                                                  
    ...                                                                                                                                                       
                                                                                                                                                       
    struct iterator{ ... }
    iterator begin() { return iterator(0, this); }         ///< return the beginning for iteration                                                     
    iterator end() { return iterator(V.size(),  this); }   ///< return the end for iteration   
}
```                                                                                                                                     ```

### Example ###

Here is a simple example to use the class:

```cpp
#include "keymap.hpp"

int main() {
  keymap_t M(5);                     // 5 is the number of buckets. 
                                     // It is suggested to be #keys 
  M.insert("Albert", 0);
  M.insert("John", 3);
  M.insert("Nikita", 1);
  
  size_t id_mary = M.find("Mary");   // id_mary=M.invalid()
  size_t id_john = M.find("John");   // id_john=3
  
  for (auto s : M)
    cout << s << "\n";
}
```

### Performance ###

```
yxia@/home/xiay/YXIA/ibmppl.gsa/tests/keymap>./test_keymap vertex_keys_uniq.txt
------------- performance ------------
execute shell command:                  "wc -l vertex_keys_uniq.txt"
number of inputs:                       2041309
building time [sec]:                    1.00145
persisting time [sec]:                  1.05706
loading time [sec]:                     0.429453
search time [sec]:                      2.88775e-07

------------- statistics -------------
number of keys:                 	2041309
L1 capacity:                    	2041309
L1 hits:                        	750774	--> (36.779%)
L2 hits:                        	1290535	--> (63.221%)
L3 hits:                        	0	--> (0%)
Number of chains in L2:         	539453
Number of chains in L3:         	0
Size of the longest chain in L2:	8
Size of the longest chain in L3:	0
Average size of all chains in L2:	2.3923
Average size of all chains in L3:	0

```


```
yinglongs-mbp:keymap yxia$ ./test_keymap vertex_keys_uniq.txt 
------------- performance ------------
execute shell command:                  "wc -l vertex_keys_uniq.txt"
number of inputs:                       2041309
building time [sec]:                    1.1231
persisting time [sec]:                  0.497462
loading time [sec]:                     0.716397
search time [sec]:                      2.97101e-07

------------- statistics -------------
number of keys:                 	2041309
L1 capacity:                    	2041309
L1 hits:                        	750774	--> (36.779%)
L2 hits:                        	1290535	--> (63.221%)
L3 hits:                        	0	--> (0%)
Number of chains in L2:         	539453
Number of chains in L3:         	0
Size of the longest chain in L2:	8
Size of the longest chain in L3:	0
Average size of all chains in L2:	2.3923
Average size of all chains in L3:	0

```
