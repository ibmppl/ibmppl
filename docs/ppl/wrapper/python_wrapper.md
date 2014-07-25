# Python Wrapper interface
The python interface exposes a set of classes encapsulating the C++ graph API. In order to access the graph methods, the user has to import the python wrapper module by `from py_shell_wrapper import *`. This will import all the classes required to perform operations on the graph. The key classes and their methods are listed below:
* Graph
* Vertex
* Edge
* Property
* Predecessor

## Graph class:
The graph class is the starting point of the interface. All operations are inherently linked through a graph instances. The graph is created by specifying the path and the name of the graph object as two string arguments to the constructor `Graph(filename, path)`.

### Loading a CSV file
A CSV (comma separated values) file can be loaded into the graph using the two utility methods `load_csv_vertices` and `load_csv_edges`. For instance
```python
g.load_csv_vertices("test_vertices.csv", True, ",",0," ",2);
g.load_csv_edges("test_edges.csv", True,",", 0,1, "EDGE",0,"na");
```
loads a graph `g` with vertices from `test_vertices.csv`, which has a header (second argument), values are comma "," separated (third argument), with key positions at column 0 (fourth argument), empty global label (fifth argument) and the vertex labels in column 2 (last argument). Once the vertices have been added, we can add the edges between the vertices from the file `test_edges.csv`. This is achieved by the method `load_csv_edges`, which is passed the filename (first argument), whether the csv file has a header (second argument), values are comma separated (third argument), source vertices are in column 0 (fourth argument), destinations are in in column 1 (fifth argument), the global label for all edges "EDGE" (sixth argument) and the edge-label positions in column 0.

### Adding vertices/edges:
We can also add vertices and edges directly to a graph using `add_vertex(label_id)` to add a vertex to a graph with a specific label `labelid` which returns a `Vertex` object. We can then add edges between vertex objects by `add_edge_ref(src_vertex, dst_vertex, edge_label)`.

### Vertex traversal
We can traverse all the vertices of the graph using the `vertices()` method of the graph. For instance, the following snippet goes over all the vertices in the graph;
```python
g = Graph(....);
#initialize graph
for v in g.vertices():
   #do something with v
```
### Utility functions
The graph class provides some utility functions to assist the user in debugging the application; `print_graph` prints the graph along with all the vertices, edges and properties to the screen whereas `create_random(num_vertices, num_edges)` populates a graph with random vertices and edges specified by `num_vertices` and `num_edges`.

## Vertex
A vertex instance encapsulates a vertex object in the graph. When a vertex is added to the graph via `add_vertex`, a vertex object is returned. Similarly when iterating over all the vertices of a graph using `vertices()`, each iteration has access to a different vertex object in the graph. A vertex object exposes most of the components of the graph;
### Properties
We can access all the properties associated with a vertex via the `properties()` method. This provides a `Property` object which encapsulates the property of the vertex.
### Edges
We can access all the edges outgoing from a vertex via `edges()` method. This provides a range of `Edge` object, which can be used to access the source and target vertex as well as any properties associated with the edge. Following is a code snippet to print all the properties of an edge;
```python
   for e in v.edges():
      for p in e.properties():
         #Do something with property p
```
### Predecessors
We can also access the predecessors of a vertex which returns `Predecessor` objects. These can be used to access the edge identifier associated with the edge via `edge_id` as well as the source vertex identifier via `source_id`
# Printing graph
Here we include a simple snippet to print all the properties of the vertices and edges of a graph:
```python
for v in g.vertices():                                                                            
      print ('Vertex id ', v.id())                                                                      
      for p in v.properties():                                                                      
         print ('Vertex property ', p.name(), p.value());                                                      
      for pred in v.predecessors():                                                                  
         print ('Predecessor: ', pred.edge_id(), pred.vertex_id() );                                        
      for e in v.edges():                                                                            
         print ('Edge target', e.target())                                                                
         for pe in e.properties():                                                                  
            print ('Edge property ', pe.name(), pe.value())            
```

# Test code 
We provide a test code in python for users to try out native store
in python environment, the code is available at [python_wrapper_test.py](python_wrapper_test.py)

# Building and running
The directory contains a makefile, which can be invoked via `make`. This
should build all the necessary components. `libleveldb.so` needs to be
on your library paths to run the wrapper. In order to test the
setup, you can run `python test.py` which should run a small test
application included in the directory (update the name of the csv files
inside the code as required). If you get an error message about
`liblevedb.so` not being found, try `LD_LIBRARY_PATH=../../lib python
test.py` which would append the `lib` folder to the library path prior
to executing the command.
