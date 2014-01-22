
###Programming style guide

We use the cpplint.py tool to do style/format checking.

You need to download depot_tools 'git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git', then add depot_tool.git/ directory to your path 

Before checking your codes, please run the presumbit tool and fix any reported formatting errors.

```bash
$ tools/presubmit.py
```
For more information on google C++ style guide, refer to http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml

###How to add tests/apps to PPL code base?

Test codes for PPL are organized as follows:
- `apps/`: for applications that use PPL library
- `tests/`: for simple tests developed to unit test PPL library
- `tests/defects/`: for defects

Each new test/apps must have a makefile with the following targets:
- `make all`: build the binary
- `make run`: run the binary
- `make verify` and `make VERIFY=1 all`: run and build the binary and verify results
- `make clean`: cleanup generated files

Please copy `${PPL_ROOT}/Makefile.template` and customize it accordingly. 

Here is an example Makefile (from `apps/gShell`):
```bash
# ROOT indicate the top-level directory of PPL
ROOT=../..
# the target binary to be built or run
TARGET=nvStore
# all the objects needed to build the target
OBJS=store_engine.hpp nvStore.o Helper.o keymap_loader.o store_manager.o socket_server.o

### the following flags are optional

# additional flags to be passed to g++ during compilation
EXTRA_CXX_FLAGS=-I../common/ -I${ROOT}/kvstore -I$(ROOT)/datastructure/graph/dbstore/ -I$(ROOT)/data
structure/graph/  -std=c++0x
# additional libraries to be passed during linking
EXTRA_LIBS=-lkvstore
# additional files or directories to be removed during 'make clean'
EXTRA_CLEANUP=nvStoreClient

# command line arguments when running target in 'make run' or 'make verify'
RUN_ARGS=interactive < test_script.txt
# directoies that are first remove and then created before 'make run' or 'make verify'
GENERATED_DIRS=database

# include all the default definition and default targets (e.g., all, run, verify, clean)
# many application tests can use the default targets in common.mk w/o having to define
# any other targets
include ${ROOT}/common.mk

# Overwrite the default 'all' target in common.mk because it builds an additional 'client' target
all: ${TARGET} client

client: nvStoreClient.o
        ${CXX} ${LINKER_OPTIONS} $< -o nvStoreClient
```
###How to run (self-verifying) tests?

Currently, all tests under `${PPL_ROOT}/apps` are self-verifying. To run a verification test: 
```bash 
make clean 
make VERIFY=1 all 
make verify 
``` 
Note that verification test requires building the binary with
`VERIFY=1` specified. This is because some tests output timing information
that differ from run to run. Since the verification is done by comparing 
the output against an expected output (i.e., `EXPECTED_OUTPUT`), 
we need to suppress time-sensitive output during verification runs.

The output of a successful verification run is:
```bash
./../../../tools/compare.sh _output.log EXPECTED_OUTPUT _diff.log
****************************************************
TEST PASSED
****************************************************
```
The output of a failed verification run is:
```bash
./../../tools/compare.sh _output.log EXPECTED_OUTPUT _diff.log
****************************************************
TEST FAILED: please check _diff.log for details
****************************************************
```
Here are the targets supported by the Makefile system:
```bash
 USAGE: make [OPTIONS] TARGET
            all: build all binaries
            run: run application (optimized version)
          clean: clean up generated files

  Valid targets are:

  Valid build OPTIONS are:
    EXTRA_FLAGS=xx : additional C/C++ flags
  EXTRA_CLEANUP=xx : additional files/dirs to be cleaned up
     EXTRA_LIBS=xx : additional libs to be linked in
           DEBUG=1 : enable debug output in ppl
    CHECK_BOUNDS=1 : enable C++ STL bounds checking

  Valid run OPTIONS are:
          NT=<n> : num of threads (for parallel version)
       BLOCK=<n> : blocking size for foreach tasks (for parallel version)
        VERIFY=1 : enable verify output in ppl
```
###Setup self-verifying tests
Self verification is done by the `make verify` target. Here is the
definition of the `verify` target defined in
`${PPL_ROOT}/common.mk`. Basically, `make run` captures the output into
a log, which is compared against an expected output file. In most
cases, the verify target provided by `common.mk` is sufficient.
```bash
verify:
        make run
        ./${ROOT}/tools/compare.sh ${OUTPUT_LOG} ${EXPECTED_LOG} ${DIFF_LOG}
```
To support `make verify` in your tests:
- The test needs to produce a verifiable output, which is saved to `EXPECTED_OUTPUT`
- `git add EXPECTED_OUTPUT`; `git commit -a`
- If the application by default produces some time-sensitive output, guard such output like this:

```C
#ifndef ENABLE_VERIFY
  printf("Timing is %d sec", end);
#endif
```

NOTE that if your test does not support verification yet, add the
following target into your makefile:
```bash
verify:
    make no-self-verify
```
In this case, `make verify` produces the following message:
```bash
******************************************
WARNING: test case has no self verification
******************************************
```
###Generate doxygen documentation

We use doxygen to generate documentations. The input files for doxygen is under <ibmppl_path>/docs/. To update the documentation, either modigy the *.txt files or doxygen annotations in the library source codes.

To publish new documentations, you need to go through the following steps:

1. Make sure you have doxygen installed

2. Checkout the gh-pages branch of your project to docs/gh-pages.github
```bash
$ add docs/gh-pages.github to .gitignore
$ cd docs
# clone the project repo to docs/gh-pages.github
$ git clone https://github.com/ibmppl/ibmppl.git gh-pages.github
$ cd gh-pages.github
$ git checkout gh-pages   # switch to the gh-pages branch of the project repo
```
  
3. Generate new doxygen pages and copy into gh-pages.github
```bash
$ cd docs
$ make         # generate documentation into docs/html
$ make gitpub  # copy docs/html into docs/gh-pages.github
$ cd gh-pages.github
$ git commit -a # checkin new documentation to github
$ git status   # to check if there is any new file (untracked)
$ manually add any new file "git add ..." and "git commit"
$ git push     # push to github
```
Note: it may take 10 minutes before the new pages appear on http://pengwuibm.github.io/ibmppl/
