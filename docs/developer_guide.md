#Developer Guide

##Programming style guide

We use the cpplint.py tool to do style/format checking.

You need to download depot_tools 'git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git', then add depot_tool.git/ directory to your path 

Before checking your codes, please run the presumbit tool and fix any reported formatting errors.

```bash
tools/presubmit.py
```
For more information on google C++ style guide, refer to http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml

##Running unit tests

<b> TBA </b>

##Generate doxygen documentation

We use doxygen to generate documentations. The input files for doxygen is under <ibmppl_path>/docs/. To update the documentation, either modigy the *.txt files or doxygen annotations in the library source codes.

To publish new documentations, you need to go through the following steps:

1. Make sure you have doxygen installed

2. Checkout the gh-pages branch of your project to docs/gh-pages.github
```bash
$ add docs/gh-pages.github to .gitignore
$ cd docs
# clone the project repo to docs/gh-pages.github
$ git clone https://github.com/pengwuibm/ibmppl.git gh-pages.github
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
