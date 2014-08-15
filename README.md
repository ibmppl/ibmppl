##High Performance Property Graph Runtime and Store
======

<i>Please contact Yinglong Xia (yxia@us.ibm.com) for trial.</i>

The IBMPPL is the kernel part of IBM System G Native Store, which provides high performance C++ graph libraries to help develop various graph applications on sequential, concurrent and/or distributed platforms. 

### Key features

- Uniformed graph interface
  + sequential
  + multithreading (concurrent)
  + distributed
- Flexible graph representation
  + graph with user defined properties 
  + subproperty on vertices/edges and indexing
- Scheduling runtime
  + for_each parallel construct
  + task graph scheduling
- Data structure abstraction 
  + graph (w/ persistency support)
  + distributed array/mapping
- Graph Key-value store
  + optimized for graph primitives
  + portable on various file systems
- Usability
  + C++ Graph APIs
  + gShell for graph query
  + server/client socket support
  + REST-like API support
  + Java TinkerPop API support
  + Gremlin Query support
  + Python API support (undergoing)
  + SPARQL frontend support (undergoing)

<!--### Examples

<b> Under Construction! </b>
-->

### More Information
- [Getting Started](docs/ppl/getting_started.md)
- [Developers' Guide](docs/ppl/developer_guide.md)
- [Property Graph Developers' Tutorial](docs/ppl/programming_guide.md)
- [Graph Library APIs/Classes](http://ibmppl.github.io/ibmppl/index.html)
- [FAQ & Trouble Shooting](docs/ppl/faq.md)
- [Users' Guide to gShell (Native Store)](docs/gShell/gShell_APIs.md)
- [Users' Guide to Graph K/V Store](docs/gKV/graphKVstore.md)
