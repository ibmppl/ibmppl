##IBM Parallel Programming Library
### --  A High Performance Property Graph Runtime and Store
======

The IBMPPL is a parallel C++ library to help develop distributed, parallel graph applications.

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
  + portable on file systems
- Usability
  + C++ Graph APIs
  + gShell for graph query
  + server/client mode support
  + REST-like API support
  + TinkPop support
  + Gremlin support

<!--### Examples

<b> Under Construction! </b>
-->

### More Information
- [Getting Started](docs/ppl/getting_started.md)
- [Developers' Guide](docs/ppl/developer_guide.md)
- [Users' Guide](docs/ppl/programming_guide.md)
- [PPL Library API](http://ibmppl.github.io/ibmppl/index.html)
- [FAQ & Trouble Shooting](docs/ppl/faq.md)
- [Users' Guide to gShell (Native Store)](docs/gShell/gShell_APIs.md)
- [Users' Guide to Graph K/V Store](docs/gKV/graphKVstore.md)
