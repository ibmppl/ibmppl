### Frequently Asked Questions

<b> Under Construction! </b>

### Trouble shooting
- Question: How do I build and run ibmppl if the systemG project gsa directory (/gsa/yktgsa-p1/09/systemg) is not mounted on my machine?
  + Answer: You need to do the following steps on your local machine:

    Install boost header file: on Linux, yum install boost; on AIX, just download latest boost library and copy the source
    Make a dataset directory by copying dataset you use from /gsa/yktgsa-p1/09/systemg/dataset/ (copying the entire dataset may be too long)
    Modify ibmppl/common.mk to specify the path to boost library header file and to your dataset directory

- Question: Fail to build the runtime w/ the following errors about thread-local storage

```bash
scheduler.cc:30: error: thread-local storage not supported for this target
make[1]: *** [scheduler] Error 1
```
   + Answer: You probably are using an old g++. Make sure your g++ version is at least 4.6.0

- Question: Fail to build the runtime w/ the following errors when compiling boost library header files

```bash
/gsa/yktgsa-p1/09/systemg/boost_1_53_0/boost/mpl/aux_/preprocessed/gcc/vector.hpp:22:8: note:   âboost::mpl::vectorâ
/gsa/yktgsa-p1/09/systemg/boost_1_53_0/boost/container/container_fwd.hpp:53:7: note:   âboost::container::vectorâ
/gsa/yktgsa-p1/09/systemg/boost_1_53_0/boost/fusion/container/vector/detail/advance_impl.hpp:30:70: error: template argument 1 is invalid
``` 
   + Answer: Try a later version of g++. This problem happens on p7curielin where the default g++ is 4.6.0, and using /opt/at5.0/bin/g++ solves the problem (v. 4.6.4)

### Known Bugs

