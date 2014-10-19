### gShell Multi-User Support Manual

Native Store [gShell (version 2)](gShellv2_APIs.md) supports multiuser
mode. The multiuser mode starts concurrent graph store services for managing a set of
graphs, possibly created by different users. The users can work on their graphs in
parallel, and share some graphs to their friends. Actually,
the users and their resources are managed by a graph in System G Native Store, nothing
essentially different from the graph created by users in gShell. The
gShellSuperMgr maintains the user graph where each vertex is an
user, and the properties on a directed edge give the graphs shared by the source
vertex to the target user.

- **How to start gShell multiuser service**

The multiuser mode can be started by:
```bash
     ./gShellSuperMgr <socket_port>
```
The expected message on your screen will be:
```bash
    $ ./gShellSuperMgr  7755
	========================================================
	  SYSTEM G NATIVE STORE GSHELL MANAGER (MULTIUSER MODE)
    ========================================================
    gShell manager starts with socket port: 7755
    start socket
```

- **How does gShell multiuser service work**

The gShell multiuser service consists of three critical parts:

  - gShellSuperMgr -- the demon code oversees the concurrently opened graph stores,
  coordindating the graph sharing between users
  - gShellClient -- the client code used by each users, which can be embedded into a
  webpage or GUI on the client side
  - gShell (hidden) -- the gShell engine for manageing graphs from a specific graph store

Basically, gShellSuperMgr will listen to any request from any
gShellClient. If the request is regarding user management or resource sharing,
gShellSuperMgr will start a gShell service internally for the corresponding
store, if not started already. The supermanager also removes inactive
users, or even cleans up the storage. If the request from the client is a
regular gShell command (see [gShellv2 tutorial](gShellv2_APIs.md)), then the
supermgr will notify the client to forward this request to a specific gShell
store service. This process is hidden to users. So, from the users's
perspective, the only explicit communication occurs between his/her client to
the gShellSuperMgr. 

- **Messges from gShellSuperMgr**

The gShellSuperMgr communicates with clients using messages through
a socket. So, it allows the server and client on different machines. The messages
are likely processed by the GUI or webpage, but in case you try to handle it
yourself (e.g., embed the client into one's code), here are some hints:

  - 1) all errors come with a number in format of "error[<num>]: <description>".
  - 2) when admin says "bye", all active users are kicked out by calling their
  "close_all". So, data should be saved
  - 3) if we quit the gshell manager by "bye", there is no defunct process
remaining in the system.
  - 4) all normal information has a prefix "success: ".
  - 5) user registration and graph sharing is persistent
  - 6) access to the shared graph is supported.

The error message list is as follows, coming with an error code and a string brief:

  - error[0]: unknown error <msg>;
  - error[1]: user is unregistered;
  - error[2]: user has not logged in;
  - error[3]: user passwd is incorrect;
  - error[4]: user exists;
  - error[5]: permission denied;
  - error[6]: graph sharing fails;
  - error[7]: insufficient parameters;
  - error[8]: the specified friend is not valid;
  - error[9]: permission denied;
  - error[10]: invalid user;

- **How to use gShell multiuser service work**

The user management commands are as follows, in addition to the regular graph
store query commands:

```bash
   bye
   register
   del_user
   login
   logout
   list_users
   add_shared_graph
   remove_shared_graph
```

Here are some examples to try. Basically, the format for using the client is:

```bash
  ./gShellClient "<command>" <username> <gShellSuperMgr_host>
  <gShellSuperMgr_port> [friend]
```

When one wants to shared a graph to someone else, the arguemnt `friend` is
provided. The graph name will be detected by `--graph` in the command.

```bash
   ./gShellClient "register tom 111" tom 127.0.0.1 7755
   ./gShellClient "list_users" tom 127.0.0.1 7755
   ./gShellClient "login tom 111" tom 127.0.0.1 7755
   ./gShellClient "login sam 222" sam 127.0.0.1 7755
   ./gShellClient "list_all" tom 127.0.0.1 7755
   ./gShellClient "list_all" sam 127.0.0.1 7755
   ./gShellClient "create --graph gsam2" sam 127.0.0.1 7755
   ./gShellClient "add_vertex --graph gsam2 --id v1" sam 127.0.0.1 7755
   ./gShellClient "add_vertex --graph gsam2 --id v2" sam 127.0.0.1 7755
   ./gShellClient "add_edge --graph gsam2 --src v1 --targ v2" sam 127.0.0.1 7755
   ./gShellClient "get_num_vertices --graph gsam2" tom 127.0.0.1 7755 sam
   ./gShellClient "get_num_vertices --graph gsam2" sam 127.0.0.1 7755
   ./gShellClient "add_shared_graph --graph gsam2" tom 127.0.0.1 7755 sam
   ./gShellClient "print_all --graph gsam2" tom 127.0.0.1 7755 tom
   ./gShellClient "bye" tom 127.0.0.1 7755
   ./gShellClient "bye" admin 127.0.0.1 7755
```

A full-featured multi-user support requires many operations and funcationalities, but I hope the
current one can work for many cases.
