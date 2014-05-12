
## Hands-on Tutorial for Native Store gShell (v2)  

### gShell version 2 Usage

gShell runs in the interactive mode, server/client mode, REST API mode, and the command-line mode. In all modes, the commands are the same or with very limited changes that can be told without introduction. In this document, we use the interactive mode as an example, which is perfect for users to operate multiple local graph stores simultaneously. 

-----------

####Grammar for Native Store gShell for Multiproperty Graph 

```bash
<command> [argKey[:sub-argKey]:argVal]
````
* <i>command</i> is a command verb defined by gShell

* <i>argKey</i> is a key of an argument, defined by gShell or user

* multiple <i>sub-argKey</i> can be applied 

* <i>argVal</i> is the corresponding value.


<b>For example:</b>

```bash
create graph:kv11     // create a graph store named kv11

list_all              // display all graph stores 

add_vertex graph:g id:"Tom" label:"Actor" prop:DoB:"1944" prop:gender:"Male"  // add a vertex with label and properties

query_vertex graph:g id:"Tom"  // query a vertex according to vertex ID

filter_vertices graph:g prop:DoB:"1944" prop:gender:"Male" out:result // find a set of vertices 

filter_vertices in:result id:"Tom"  // second find
````

_question: how to build the map for prop:Dob and prop:gender? build a secondary map?

_question: how to handle user-defined IDs? is it a property or we build an internal map from string to vid

-----------

####We use the example from Neo4j Tutorial to show how to use Native Store gShell

The description of each bullet below comes from Neo4j Tutorial example. We display the both solutions from Neo4j Cypher and Native Store gShell, for illustrating how much they can be mapped to each other. Our CLI-style makes queries more compact, clearer, and easier for embedded use.  

- Create a node for the actor Tom Hanks:

```bash
CREATE (n:Actor { name:"Tom Hanks" });
````

```bash
add_vertex graph:g id:"Tom Hanks" label:"Actor"
````
<sup>* gShell allows interleave multiple graphs, so we must explictly specify the graph name (e.g. "g") for each  graph operation commands.</sup><br>
<sup>* gShell accepts vertex ID string as a default vertex property.</sup>

- Let’s find the node we created:

```bash
MATCH (actor:Actor { name: "Tom Hanks" })
RETURN actor;
````

```bash
filter_vertices graph:g label:"Actor" ID:"Tom Hanks"
````

- Now let’s create a movie and connect it to the Tom Hanks node with an ACTED_IN relationship:

```bash
MATCH (actor:Actor)
WHERE actor.name = "Tom Hanks"
CREATE (movie:Movie { title:'Sleepless IN Seattle' })
CREATE (actor)-[:ACTED_IN]->(movie);
````
```bash
add_vertex graph:g id:"Sleepless IN Seattle" label:Movie
add_edge graph:g src:"Tom Hanks" targ:"Sleepless IN Seattle" label:"ACTED_IN"
````

- Set a property on a node:

```bash
MATCH (actor:Actor { name: "Tom Hanks" })
SET actor.DoB = 1944
RETURN actor.name, actor.DoB;
````
```bash
add_subprop graph:g id:"Tom Hanks" prop:DoB:"1944"
````

- The labels Actor and Movie help us organize the graph. Let’s list all Movie nodes:

```bash
MATCH (movie:Movie)
RETURN movie AS `All Movies`;
````
```bash
filter_vertices graph:g label:Movie
````

- We’ll go with three movies and three actors:

```bash
CREATE (matrix1:Movie { title : 'The Matrix', year : '1999-03-31' })
CREATE (matrix2:Movie { title : 'The Matrix Reloaded', year : '2003-05-07' })
CREATE (matrix3:Movie { title : 'The Matrix Revolutions', year : '2003-10-27' })
CREATE (keanu:Actor { name:'Keanu Reeves' })
CREATE (laurence:Actor { name:'Laurence Fishburne' })
CREATE (carrieanne:Actor { name:'Carrie-Anne Moss' })
CREATE (keanu)-[:ACTS_IN { role : 'Neo' }]->(matrix1)
CREATE (keanu)-[:ACTS_IN { role : 'Neo' }]->(matrix2)
CREATE (keanu)-[:ACTS_IN { role : 'Neo' }]->(matrix3)
CREATE (laurence)-[:ACTS_IN { role : 'Morpheus' }]->(matrix1)
CREATE (laurence)-[:ACTS_IN { role : 'Morpheus' }]->(matrix2)
CREATE (laurence)-[:ACTS_IN { role : 'Morpheus' }]->(matrix3)
CREATE (carrieanne)-[:ACTS_IN { role : 'Trinity' }]->(matrix1)
CREATE (carrieanne)-[:ACTS_IN { role : 'Trinity' }]->(matrix2)
CREATE (carrieanne)-[:ACTS_IN { role : 'Trinity' }]->(matrix3)
````

```bash
add_vertex graph:g id:"The Matrix" label:Movie prop:year:"1999-03-31"
add_vertex graph:g id:"The Matrix Reloaded" label:Motive prop:year:"2003-05-07"
add_vertex graph:g id:"The Matrix Revoluations" label:Motive prop:year:"2003-10-27"
add_vertex graph:g id:"Keanu Reeves" label:Actor
add_vertex graph:g id:"Laurence Fishburne" label:Actor
add_vertex graph:g id:"Carrie-Anne Moss" label:Actor
add_edge graph:g src:"Keanu Reeves" targ:"The Matrix" label:ACTS_IN prop:role:"Neo"
add_edge graph:g src:"Keanu Reeves" targ:"The Matrix Reloaded" label:ACTS_IN prop:role:"Neo"
add_edge graph:g src:"Keanu Reeves" targ:"The Matrix Revoluations" label:ACTS_IN prop:role:"Neo"
add_edge graph:g src:"Laurence Fishburne" targ:"The Matrix" label:ACTS_IN prop:role:"Morpheus"
add_edge graph:g src:"Laurence Fishburne" targ:"The Matrix Reloaded" label:ACTS_IN prop:role:"Morpheus"
add_edge graph:g src:"Laurence Fishburne" targ:"The Matrix Revoluation" label:ACTS_IN prop:role:"Morpheus"
add_edge graph:g src:"Carrie-Anne" targ:"The Matrix" label:ACTS_IN prop:role:"Trinity"
add_edge graph:g src:"Carrie-Anne" targ:"The Matrix Reloaded" label:ACTS_IN prop:role:"Trinity"
add_edge graph:g src:"Carrie-Anne" targ:"The Matrix Revoluation" label:ACTS_IN prop:role:"Trinity"
````

- Let’s check how many nodes we have now:

```bash
MATCH (n)
RETURN "Hello Graph with " + count(*)+ " Nodes!" AS welcome;
````
```bash
get_num_vertices graph:g
````

- Return a single node, by name:

```bash
MATCH (movie:Movie { title: 'The Matrix' })
RETURN movie;
````
```bash
query_vertex graph:g id:"The Matrix"
````

- Return the title and date of the matrix node:

```bash
MATCH (movie:Movie { title: 'The Matrix' })
RETURN movie.title, movie.year;
````
```bash
query_vertex graph:g id:"The Matrix"  prop:year
````
<sup>* query_vertex always outputs the id. When specifying props, it shows the selected properties; otherwise, all props are shown.</sup><Br>
<sup>* This can also be solved using filter_vertices. See the next example for hints.</sup>

- Show all actors:

```bash
MATCH (actor:Actor)
RETURN actor;
````
```bash
filter_vertices graph:g label:Actor
````

- Return just the name, and order them by name:

```bash
MATCH (actor:Actor)
RETURN actor.name
ORDER BY actor.name;
````
```bash
g filter_vertices label:Actor
??? output[??] sort vertex name
````

- Count the actors:

```bash
MATCH (actor:Actor)
RETURN count(*);
````
```bash
g filter_vertices label:Actor
??? output[??] count vertex
````

- Get only the actors whose names end with “s”:

```bash
MATCH (actor:Actor)
WHERE actor.name =~ ".*s$"
RETURN actor.name;
````
```bash
???
````

- Count nodes:

```bash
MATCH (n)
RETURN count(*);
````
```bash
g get_num_vertices
````

- Count relationship types:

```bash
MATCH (n)-[r]->()
RETURN type(r), count(*);
````

```bash
g filter_edges label:r
output[??] count
````

- List all nodes and their relationships:

```bash
MATCH (n)-[r]->(m)
RETURN n AS FROM , r AS `->`, m AS to;
````
```bash
g filter_edges	// no constraint
````

- Here’s how to add a node for yourself and return it, let’s say your name is “Me”:

```bash
CREATE (me:User { name: "Me" })
RETURN me;
````
```bash
g add_vertex "Me" label:User
````

- Let’s check if the node is there:

```bash
MATCH (me:User { name: "Me" })
RETURN me.name;
````
```bash
g query_vertex "Me"
````

- Add a movie rating:

```bash
MATCH (me:User { name: "Me" }),(movie:Movie { title: "The Matrix" })
CREATE (me)-[:RATED { stars : 5, comment : "I love that movie!" }]->(movie);
````
```bash
g add_edge "Me" "The Matrix" label:REATED stars:5 comment:"I love that movie!"
````

- Which movies did I rate?

```bash
MATCH (me:User { name: "Me" }),(me)-[rating:RATED]->(movie)
RETURN movie.title, rating.stars, rating.comment;
````
```bash
g find_neighbors "Me" 
???
````

- We need a friend!

```bash
CREATE (friend:User { name: "A Friend" })
RETURN friend;
````
```bash
g add_vertex "A Friend" label:User
````

- Add our friendship idempotently, so we can re-run the query without adding it several times. We return the relationship to check that it has not been created several times.

```bash
MATCH (me:User { name: "Me" }),(friend:User { name: "A Friend" })
CREATE UNIQUE (me)-[friendship:FRIEND]->(friend)
RETURN friendship;
````
```bash
g add_edge "Me" "A Friend" label:FRIEND
````

- Let’s update our friendship with a since property:

MATCH (me:User { name: "Me" })-[friendship:FRIEND]->(friend:User { name: "A Friend" })
SET friendship.since='forever'
RETURN friendship;

Let’s pretend us being our friend and wanting to see which movies our friends have rated.

MATCH (me:User { name: "A Friend" })-[:FRIEND]-(friend)-[rating:RATED]->(movie)
RETURN movie.title, avg(rating.stars) AS stars, collect(rating.comment) AS comments, count(*);

That’s too little data, let’s add some more friends and friendships.

MATCH (me:User { name: "Me" })
FOREACH (i IN range(1,10)| CREATE (friend:User { name: "Friend " + i }),(me)-[:FRIEND]->(friend));

Show all our friends:

MATCH (me:User { name: "Me" })-[r:FRIEND]->(friend)
RETURN type(r) AS friendship, friend.name;

All other movies that actors in “The Matrix” acted in ordered by occurrence:

MATCH (:Movie { title: "The Matrix" })<-[:ACTS_IN]-(actor)-[:ACTS_IN]->(movie)
RETURN movie.title, count(*)
ORDER BY count(*) DESC ;

Let’s see who acted in each of these movies:

MATCH (:Movie { title: "The Matrix" })<-[:ACTS_IN]-(actor)-[:ACTS_IN]->(movie)
RETURN movie.title, collect(actor.name), count(*) AS count
ORDER BY count DESC ;

What about co-acting, that is actors that acted together:

MATCH (:Movie { title: "The Matrix"
  })<-[:ACTS_IN]-(actor)-[:ACTS_IN]->(movie)<-[:ACTS_IN]-(colleague)
RETURN actor.name, collect(DISTINCT colleague.name);

Who of those other actors acted most often with anyone from the matrix cast?

MATCH (:Movie { title: "The Matrix"
  })<-[:ACTS_IN]-(actor)-[:ACTS_IN]->(movie)<-[:ACTS_IN]-(colleague)
RETURN colleague.name, count(*)
ORDER BY count(*) DESC LIMIT 10;

We know that Trinity loves Neo, but how many paths exist between their actors? We’ll limit the path length and the query as it exhaustively searches the graph otherwise

MATCH p =(:Actor { name: "Keanu Reeves" })-[:ACTS_IN*0..5]-(:Actor { name: "Carrie-Anne Moss" })
RETURN p, length(p)
LIMIT 10;

Bur that’s a lot of data, we just want to look at the names and titles of the nodes of the path.

MATCH p =(:Actor { name: "Keanu Reeves" })-[:ACTS_IN*0..5]-(:Actor { name: "Carrie-Anne Moss" })
RETURN extract(n IN nodes(p)| coalesce(n.title,n.name)) AS `names AND titles`, length(p)
ORDER BY length(p)
LIMIT 10;

