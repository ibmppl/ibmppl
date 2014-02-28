### Interface of Graph Key-Value Stores in Native Store

System G Native Store utilizes an alternated key-value store as the backend for persisting in-memory graph data, including both the graph structure and the properties on vertices and edges. This document specifies the interfaces of the graph K/V store. The interfaces are implemented using C++ natively, although they can be implemented up on any standard K/V stores with some additional efforts. 

Graph K/V store consists of a collection of key-value pairs, where each pair has a key in type of stl::string; each value is a set of property bundles (similar to column family in HBase) and each property bundle is a list of fix-sized buffers. The buffer content is agonstic to graph K/V store, but taken care by users, such as a set of serialized key-value pairs. The user are allowed to speicify the buffer unit size. A large size may result in more unused disk spaces; a small size may degrade the query performance. 

<b> Basic operations </b>

- Create a graph K/V store. Assuming we want to create a store, we must specify the name by <store_name> (path can be included). The second argument gives the number of property bundles by the size of a vector called <bundle_blk_sz>; each element in the vector gives the siz eof the buffer unit in the corresponding bundle. 

```bash
  kvStore_t create(string store_name, vector<size_t> bundle_blk_sz);
```
- Open an existing store or close an opened store are straighforward.

```bash
  kvStore_t open(string store_name);
  void      close();
```

- Query the value in a property bundle, given a key. This is a basic key-value query, but the bundle index must be given. The type key_t by default is a stl::string.


```bash
  void find(key_t key, void *databuf, size_t bufsz, size_t &datasz, size_t bundle_index); 
```

- Insert/Update a value. If the key is not in the store, it is created and the corresponding value is added to a bundle; otherwise, the corresponding value is inserted/updated. The ohter bundles are initialized as empty or remain unchanged.

```bash
  void insert(key_t key, void *databuf, size_t datasz, size_t bundle_index);
```

- Append data to the end of a bundle buffer. If <key> does not exist, it is created and the value in the databuf is copied to the bundle specified by <bundle_index>. If the bundle is not empty, the data is added to the end of the buffer. This is equivalent to query the value first and then store with the argumented value to the same key. However, the API is provided for performance reasons.

```bash
  void append(key_t key, void *databuf, size_t datasz, size_t bundle_index);
```

- Delete a key. If the index is specified, delete the value in the corresponding property bundle. If not, all bundles of this key is removed.

```bash
  void erase(key_t key, [size_t bundle_index])
```

<b> Multiversioning and Bi-temp </b>

Each key has a version (time stamp) cursor. By default, it is the latest version. By using the following APIs, we can retrieve data from earlier versions, or set all keys to a particular version. This is helpful for auditting a graph at a particular historic time. Any operations (see the previous section) will only affect the version matches the version cursor. It is up on the user's code if the historic data can be altered or not.

- Create a new version for a particular key. This creates a new version and the latest version before this invocation becomes an old version. The version number can be assigned by user, but will be checked internally to ensure versions monotoneously increasing. By default, the version is derived from the current time stamp.

```bash
  bool generate_new_version(key_t key [, version_t ver]);
```

- Set the version number of a key for data access. All keys are at the latest version after creating/loading a store. The following APIs move the version cursor. If it reaches the earlier (latest) version, goto_previous (goto_next) will not function.

```bash
  bool goto_latest(key_t key);
  bool goto_first(key_t key);
  bool goto_previous(key_t key);
  bool goto_next(key_t key);
```

- Get number of versions a key has. Note that different keys may have different number of versions.

```bash
  int get_num_versions(key_t key); 
``` 
  
- Retrive the current version number of a key; set a key to a particular version for lateron data access. The version_t can be the type of time stamp or a nonnegative number. 

```bash
  version_t get_current_version(key_t key);
  bool      goto_version(key_t key, version_t v);
```

- Go to a version approximately, when the specified version does not exist

```bash
  bool goto_version(key_t key, version_t v, const Compare& comp=Compare())
```

- Set all keys into a particular version (approximately) for batch operations. This will take time for large stores, but afterward there is no repeated version seeking in analytics. The overall execution time may be lower.

```bash
  void goto_latest_all();
  void goto_first_all();
  void goto_version_all(version_t v);
  void goto_version_all(version_t v, const Compare& comp=Compare());
```

Bi-temp feature is coming.
				  
