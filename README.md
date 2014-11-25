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
  + Python API support 
  + SPARQL frontend support (undergoing)

<!--### Examples

<b> Under Construction! </b>
-->

### More Information
- [Getting Started](docs/ppl/getting_started.md)
- [Developers' Guide in General](docs/ppl/developer_guide.md)
- [Developers' Guide to Property Graph](docs/ppl/programming_guide.md)
- [Python Wrapper to Property Graph](docs/ppl/wrapper/python_wrapper.md) 
- [APIs/Classes in Graph Library](http://ibmppl.github.io/ibmppl/index.html)
- [Users' Guide to gShell](docs/gShell/gShellv2.2_APIs.md)
- [Developers' Guide to gShell](docs/gShell/gShellv2_develop_guide.md)
- [Developers' Guide to Graph K/V Store](docs/gKV/graphKVstore.md)
- [FAQ & Trouble Shooting](docs/ppl/faq.md)
