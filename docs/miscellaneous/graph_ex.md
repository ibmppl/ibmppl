## APIs for operating multiversioning graphs
- Add a new vertex:

```bash
vertexd_t g.add_vertex(vertex_property vp [, bool start_new_version=false]);
```

- Add a new edge:

```bash
edged_t g.add_edge(vertexd_t src_vid, vertexd_t targ_vid [, bool start_new_version=false]);
```

- Find vertex:
```bash
vertex_iterator vit = g.find_vertex(vertexd_t vid [, bool enable_version_cursor=false]);
```

- Vertex/edge iterator: the same as before

- Graph traversal using "vertices_begin/vertices_end" can only access current version.

- Get vertex/edge property: the same as before

- Set vertex property: cannot change history version
```bash
vit->set_property(vertex_property vp [, bool start_new_version=false]);
```

- Set edge property: cannot change history version
```bash
eit->set_property(edge_property ep [, bool start_new_version=false]);
```

- Get number of versions a vertex has:
```bash
size_t g.get_num_versions(vertexd_t vid);
```

- Version cursor operations:
```bash
bool g.versionCursor_prev(vertexd_t vid);
bool g.versionCursor_next(vertexd_t vid);
bool g.versionCursor_latest(vertexd_t vid);
bool g.versionCursor_earliest(vertexd_t vid);

version_t g.versionCursor_curr(vertexd_t vid);
bool g.versionCursor_set(version_t ver);

void g.versionCursor_all_latest(void);
void g.versionCursor_all_earliest(void);
void g.versionCursor_all_set(version_t ver);
```

## Batch mode operations
- Enter batch mode:
```bash
bool g.batch_mode_begin(size_t batch_size);
````

- Exit batch mode:
```bash
bool g.batch_mode_end(void);
```

- In batch mode, the graph is write-only. Only following two functions are enabled:

```bash
add_vertex(); add_edge();
```
