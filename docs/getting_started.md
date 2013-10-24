
### Get the source

Send email to Xavier R Guerin to gain access to SystemG project gsa

```bash
git clone file:////gsa/yktgsa/projects/s/systemg/GIT/ibmppl
```
The library contains the following source directories:
- datastructure/ : implementation of graph abstraction
- runtime/: implementation of the task and scheduling runtime
- kvstore/: implementation of key-value store
- examples/: simple examples using ibmppl interface
- apps/: applications using ibmppl interface
- docs/: documentation
- libs/: libraries built out of ibmppl
- tools/: tools for developers

### Buildi and test the library

Recommend to use g++-4.6.4 or later versions.

You can build ibmppl on x86-linux, ppc-linux, and ppc-aix. You need to use gnu make

```bash
cd ibmppl
gmake all  /* to build the library and the examples */
gmake run /* to run all the examples */
```

At each level, you can type 'make help' to get help message. Here is the top-level help message

```bash
USAGE: make [OPTIONS] TARGET
            all: build all binaries
            run: run application (optimized version)
       run_base: run original version of the application
   run_parallel: run parallel version of the application
          clean: clean generated files

  valid targets are:

  valid OPTIONs are:
        DEBUG=1 : enable debug output in ppl
       VERIFY=1 : enable verify output in ppl
         NT=<n> : num of threads (for run_parallel)
      BLOCK=<n> : blocking size for foreach tasks (for run_parallel)
```

<b> Run examples </b>

```bash
cd ibmppl
make lib /* make the libraries */
cd examples
make all /* build the examples */
make run /* run the examples */
```

<b> Run applications</b>

<b>TBA </b>

### Use the library

<b> TBA </b>
