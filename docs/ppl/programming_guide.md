 
<b>For detailed interface specification, refer to [IBM PPL library API] (http://ibmppl.github.io/ibmppl/index.html) </b>

<b> What is an in-disk graph? </b>

e.g.,
  - describe 3 types of graphs (UNDIRECTD, DIRECTED, PRED_DIRECTED)
  - what are properties and volatile properties and the difference between the two

<b> How to construct an in-disk graph? </b>

e.g., 
  - please add a note on the importance of properly closing a in-disk graph
  - when is it necessary to provide serialize and deserialize functions for vertex and edge properties
  - which function to call to properly set vertex/edge property (in memory and on disk), how/when to use set_property_volatile

<b> How graphs are stored on disk </b>

e.g., 
  - how is consistency between graphs stored in the file system and in-memory graph maintained
  - is there a map between external vertex label (key) and internal vertex id, or does the user (writer of the analytic) need to create and maintain one himself

<b> How to open/load an in-disk graph </b>

e.g., 
  - how to correctly access information stored in an in-disk graph, whether need to call find_vertex for each vertex explicitly in order to bring its information into memory, or whether can simply traverse the graph using vertex iterator
  - what is the proper way to detect in the code whether a graph already exists on disk

<b> Memory management of inDisk graph </b>

e.g., what happens when a graph runs out of memory. Does the system automatically kick out vertices to make room 
for new vertices? 
e.g., can users explicitly unload a vertex or property from memory

<b> Other basic operations on inDiskGraph</b>

<b> How does the inDiskGraph interface differ from the basic in-memory graph interface? </b>

e.g., are there certain operations that are allowed on in-memory graph interface but not on inDiskGraph interface?

<b> Any performance considerations when using inDiskGraph </b>

e.g., Are there operations that are specially expensive?

