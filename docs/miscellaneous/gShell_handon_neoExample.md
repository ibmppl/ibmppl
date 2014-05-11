###We use the example from Neo4j Tutorial to show how to use Native Store gShell

Create a node for the actor Tom Hanks:

```bash
CREATE (n:Actor { name:"Tom Hanks" });
````

Let’s find the node we created:

MATCH (actor:Actor { name: "Tom Hanks" })
RETURN actor;

Now let’s create a movie and connect it to the Tom Hanks node with an ACTED_IN relationship:

MATCH (actor:Actor)
WHERE actor.name = "Tom Hanks"
CREATE (movie:Movie { title:'Sleepless IN Seattle' })
CREATE (actor)-[:ACTED_IN]->(movie);

Set a property on a node:

MATCH (actor:Actor { name: "Tom Hanks" })
SET actor.DoB = 1944
RETURN actor.name, actor.DoB;

The labels Actor and Movie help us organize the graph. Let’s list all Movie nodes:

MATCH (movie:Movie)
RETURN movie AS `All Movies`;

We’ll go with three movies and three actors:

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


Let’s check how many nodes we have now:

MATCH (n)
RETURN "Hello Graph with " + count(*)+ " Nodes!" AS welcome;

Return a single node, by name:

MATCH (movie:Movie { title: 'The Matrix' })
RETURN movie;


Return the title and date of the matrix node:

MATCH (movie:Movie { title: 'The Matrix' })
RETURN movie.title, movie.year;

Show all actors:

MATCH (actor:Actor)
RETURN actor;

Return just the name, and order them by name:

MATCH (actor:Actor)
RETURN actor.name
ORDER BY actor.name;

Count the actors:

MATCH (actor:Actor)
RETURN count(*);


Get only the actors whose names end with “s”:

MATCH (actor:Actor)
WHERE actor.name =~ ".*s$"
RETURN actor.name;


Count nodes:

MATCH (n)
RETURN count(*);

Count relationship types:

MATCH (n)-[r]->()
RETURN type(r), count(*);

List all nodes and their relationships:

MATCH (n)-[r]->(m)
RETURN n AS FROM , r AS `->`, m AS to;

So far, we queried the movie data; now let’s update the graph too.

Here’s how to add a node for yourself and return it, let’s say your name is “Me”:

CREATE (me:User { name: "Me" })
RETURN me;

Let’s check if the node is there:

MATCH (me:User { name: "Me" })
RETURN me.name;

Add a movie rating:

MATCH (me:User { name: "Me" }),(movie:Movie { title: "The Matrix" })
CREATE (me)-[:RATED { stars : 5, comment : "I love that movie!" }]->(movie);

Which movies did I rate?

MATCH (me:User { name: "Me" }),(me)-[rating:RATED]->(movie)
RETURN movie.title, rating.stars, rating.comment;

We need a friend!

CREATE (friend:User { name: "A Friend" })
RETURN friend;

Add our friendship idempotently, so we can re-run the query without adding it several times. We return the relationship to check that it has not been created several times.

MATCH (me:User { name: "Me" }),(friend:User { name: "A Friend" })
CREATE UNIQUE (me)-[friendship:FRIEND]->(friend)
RETURN friendship;

Let’s update our friendship with a since property:

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

