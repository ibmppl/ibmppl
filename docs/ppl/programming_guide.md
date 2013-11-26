 
<b>For detailed interface specification, refer to [IBM PPL library API] (http://pengwuibm.github.io/ibmppl/index.html) </b>

<b> What is a in-disk graph? </b>

e.g.,
  - describe 3 types of graphs (UNDIRECTD, DIRECTED, PRED_DIRECTED)
  - what are properties and volatile properties and the difference between the two

<b> How to construct an in-disk graph? </b>

e.g., please add a note on the importance of properly closing a in-disk graph

<b> How graphs are stored on disk </b>

e.g., How is consistency between graphs stored in the file system and in-memory graph maintained

<b> Memory management of inDisk graph </b>

e.g., what happens when a graph runs out of memory. Does the system automatically kick out vertices to make room 
for new vertices? 
e.g., can users explicitly unload a vertex or property from memory

<b> other basic operations on inDiskGraph</b>

