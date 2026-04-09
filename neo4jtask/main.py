
import time
from neo4j import GraphDatabase

#connection to neo
URI      = "http://localhost:7474"
USER     = "neo4j"
PASSWORD = "password123"


def wait_for_neo4j(driver, retries=15, delay=3):
    
    for attempt in range(1, retries + 1):
        try:
            driver.verify_connectivity()
            
            return
        except Exception:
            print(f"  Waiting for Neo4j... attempt {attempt}/{retries}")
            time.sleep(delay)
    raise RuntimeError("Neo4j did not become available in time.")




#creating nodes,relationships and prop.
# Dataset: Movie Character Interaction Graph (Batman Trilogy)
# Nodes: Movies, Actors, Characters
# Relationships: APPEARS_IN, PLAYED_BY, INTERACTS_WITH
CREATE_MOVIES = """
MERGE (m1:Movie {title: 'Batman Begins',          year: 2005, genre: 'Action'})
MERGE (m2:Movie {title: 'The Dark Knight',        year: 2008, genre: 'Action'})
MERGE (m3:Movie {title: 'The Dark Knight Rises',  year: 2012, genre: 'Action'})
"""

CREATE_ACTORS = """
MERGE (a1:Actor {name: 'Christian Bale',   nationality: 'British'})
MERGE (a2:Actor {name: 'Heath Ledger',     nationality: 'Australian'})
MERGE (a3:Actor {name: 'Gary Oldman',      nationality: 'British'})
MERGE (a4:Actor {name: 'Tom Hardy',        nationality: 'British'})
MERGE (a5:Actor {name: 'Anne Hathaway',    nationality: 'American'})
MERGE (a6:Actor {name: 'Aaron Eckhart',    nationality: 'American'})
"""

CREATE_CHARACTERS = """
MERGE (c1:Character {name: 'Bruce Wayne',   role: 'hero',    age: 35})
MERGE (c2:Character {name: 'Joker',         role: 'villain', age: 40})
MERGE (c3:Character {name: 'Jim Gordon',    role: 'ally',    age: 50})
MERGE (c4:Character {name: 'Bane',         role: 'villain', age: 38})
MERGE (c5:Character {name: 'Selina Kyle',  role: 'anti-hero',age: 28})
MERGE (c6:Character {name: 'Harvey Dent',  role: 'ally',    age: 36})
"""

CREATE_APPEARS_IN = """
MATCH (c:Character {name: 'Bruce Wayne'}),  (m:Movie {title: 'Batman Begins'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Bruce Wayne'}),  (m:Movie {title: 'The Dark Knight'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Bruce Wayne'}),  (m:Movie {title: 'The Dark Knight Rises'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Joker'}),        (m:Movie {title: 'The Dark Knight'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Jim Gordon'}),   (m:Movie {title: 'Batman Begins'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Jim Gordon'}),   (m:Movie {title: 'The Dark Knight'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Jim Gordon'}),   (m:Movie {title: 'The Dark Knight Rises'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Bane'}),         (m:Movie {title: 'The Dark Knight Rises'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Selina Kyle'}),  (m:Movie {title: 'The Dark Knight Rises'})
MERGE (c)-[:APPEARS_IN]->(m)

MATCH (c:Character {name: 'Harvey Dent'}),  (m:Movie {title: 'The Dark Knight'})
MERGE (c)-[:APPEARS_IN]->(m)
"""

CREATE_PLAYED_BY = """
MATCH (c:Character {name: 'Bruce Wayne'}),  (a:Actor {name: 'Christian Bale'})
MERGE (c)-[:PLAYED_BY]->(a)

MATCH (c:Character {name: 'Joker'}),        (a:Actor {name: 'Heath Ledger'})
MERGE (c)-[:PLAYED_BY]->(a)

MATCH (c:Character {name: 'Jim Gordon'}),   (a:Actor {name: 'Gary Oldman'})
MERGE (c)-[:PLAYED_BY]->(a)

MATCH (c:Character {name: 'Bane'}),         (a:Actor {name: 'Tom Hardy'})
MERGE (c)-[:PLAYED_BY]->(a)

MATCH (c:Character {name: 'Selina Kyle'}),  (a:Actor {name: 'Anne Hathaway'})
MERGE (c)-[:PLAYED_BY]->(a)

MATCH (c:Character {name: 'Harvey Dent'}),  (a:Actor {name: 'Aaron Eckhart'})
MERGE (c)-[:PLAYED_BY]->(a)
"""

CREATE_INTERACTIONS = """
MATCH (c1:Character {name: 'Bruce Wayne'}), (c2:Character {name: 'Joker'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 8, type: 'confrontation', intensity: 'high'}]->(c2)

MATCH (c1:Character {name: 'Bruce Wayne'}), (c2:Character {name: 'Jim Gordon'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 12, type: 'alliance', intensity: 'medium'}]->(c2)

MATCH (c1:Character {name: 'Bruce Wayne'}), (c2:Character {name: 'Bane'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 6, type: 'confrontation', intensity: 'high'}]->(c2)

MATCH (c1:Character {name: 'Bruce Wayne'}), (c2:Character {name: 'Selina Kyle'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 9, type: 'alliance', intensity: 'medium'}]->(c2)

MATCH (c1:Character {name: 'Joker'}),       (c2:Character {name: 'Harvey Dent'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 4, type: 'manipulation', intensity: 'high'}]->(c2)

MATCH (c1:Character {name: 'Jim Gordon'}),  (c2:Character {name: 'Harvey Dent'})
MERGE (c1)-[:INTERACTS_WITH {scenes: 5, type: 'alliance', intensity: 'low'}]->(c2)
"""


def task1_create(session):
    

    for query in [CREATE_MOVIES, CREATE_ACTORS, CREATE_CHARACTERS,
                  CREATE_APPEARS_IN, CREATE_PLAYED_BY, CREATE_INTERACTIONS]:
        # Split on blank lines so multi-line MATCH...MERGE blocks stay together
        import re
        statements = [s.strip() for s in re.split(r'\n\s*\n', query.strip()) if s.strip()]
        for stmt in statements:
            session.run(stmt)

    # Verify counts
    movies     = session.run("MATCH (m:Movie)     RETURN count(m) AS n").single()["n"]
    actors     = session.run("MATCH (a:Actor)     RETURN count(a) AS n").single()["n"]
    characters = session.run("MATCH (c:Character) RETURN count(c) AS n").single()["n"]
    rels       = session.run("MATCH ()-[r]->()    RETURN count(r) AS n").single()["n"]

    print(f"  Movies created:     {movies}")
    print(f"  Actors created:     {actors}")
    print(f"  Characters created: {characters}")
    print(f"  Relationships:      {rels}")


#deletation

def task2_delete(session):
    print("\n  deletation task:")
    

    # 1-Remove the 'age' property from Harvey Dent
    session.run("""
        MATCH (c:Character {name: 'Harvey Dent'})
        REMOVE c.age
    """)
    age_gone = session.run("""
        MATCH (c:Character {name: 'Harvey Dent'})
        RETURN c.age AS age
    """).single()["age"]
    print(f"  Harvey Dent 'age' after REMOVE: {age_gone}  (None = deleted ✓)")

    # 2-Delete the INTERACTS_WITH relationship between Gordon and Harvey Dent
    session.run("""
        MATCH (c1:Character {name: 'Jim Gordon'})-[r:INTERACTS_WITH]->(c2:Character {name: 'Harvey Dent'})
        DELETE r
    """)
    remaining = session.run("""
        MATCH (c1:Character {name: 'Jim Gordon'})-[r:INTERACTS_WITH]->(c2:Character {name: 'Harvey Dent'})
        RETURN count(r) AS n
    """).single()["n"]
    print(f"  Gordon→Harvey INTERACTS_WITH remaining: {remaining}  (0 = deleted ✓)")

    # 3-Delete Harvey Dent node 
    session.run("""
        MATCH (c:Character {name: 'Harvey Dent'})
        DETACH DELETE c
    """)
    still_there = session.run("""
        MATCH (c:Character {name: 'Harvey Dent'})
        RETURN count(c) AS n
    """).single()["n"]
    print(f"  Harvey Dent node remaining: {still_there}  (0 = deleted ✓)")


#updating

def task3_update(session):
    print("\n  updating task:")
    

    # 1-Update Bruce Wayne's age and add a new property
    session.run("""
        MATCH (c:Character {name: 'Bruce Wayne'})
        SET c.age = 37, c.alias = 'Batman', c.status = 'active'
    """)
    bruce = session.run("""
        MATCH (c:Character {name: 'Bruce Wayne'})
        RETURN c.age AS age, c.alias AS alias, c.status AS status
    """).single()
    print(f"  Bruce Wayne updated → age: {bruce['age']}, alias: {bruce['alias']}, status: {bruce['status']}")

    # 2-Update the 'intensity' property on Bruce↔Joker interaction
    session.run("""
        MATCH (:Character {name: 'Bruce Wayne'})-[r:INTERACTS_WITH]->(:Character {name: 'Joker'})
        SET r.scenes = 10, r.intensity = 'extreme'
    """)
    rel = session.run("""
        MATCH (:Character {name: 'Bruce Wayne'})-[r:INTERACTS_WITH]->(:Character {name: 'Joker'})
        RETURN r.scenes AS scenes, r.intensity AS intensity
    """).single()
    print(f"  Bruce↔Joker relationship updated → scenes: {rel['scenes']}, intensity: {rel['intensity']}")

    # 3-Update The Dark Knight movie rating
    session.run("""
        MATCH (m:Movie {title: 'The Dark Knight'})
        SET m.rating = 9.0, m.box_office_millions = 1005
    """)
    movie = session.run("""
        MATCH (m:Movie {title: 'The Dark Knight'})
        RETURN m.rating AS rating, m.box_office_millions AS box_office
    """).single()
    print(f"  'The Dark Knight' updated → rating: {movie['rating']}, box office: ${movie['box_office']}M")


#finding nodes with conditions

def task4_find_nodes(session):
    print("\n  find nodes task:")
    

    # 1-All villain characters
    print("\n  [4a] Villain characters:")
    result = session.run("""
        MATCH (c:Character {role: 'villain'})
        RETURN c.name AS name, c.age AS age
        ORDER BY c.name
    """)
    for r in result:
        print(f"    • {r['name']}  (age: {r['age']})")

    # 2-Movies released after 2006
    print("\n  [4b] Movies released after 2006:")
    result = session.run("""
        MATCH (m:Movie)
        WHERE m.year > 2006
        RETURN m.title AS title, m.year AS year
        ORDER BY m.year
    """)
    for r in result:
        print(f"    • {r['title']} ({r['year']})")

    # 3-British actors
    print("\n  [4c] British actors:")
    result = session.run("""
        MATCH (a:Actor {nationality: 'British'})
        RETURN a.name AS name
        ORDER BY a.name
    """)
    for r in result:
        print(f"    • {r['name']}")

    # 4-Characters that appear in more than one movie
    print("\n  [4d] Characters appearing in 2+ movies:")
    result = session.run("""
        MATCH (c:Character)-[:APPEARS_IN]->(m:Movie)
        WITH c, count(m) AS movie_count
        WHERE movie_count >= 2
        RETURN c.name AS name, movie_count
        ORDER BY movie_count DESC
    """)
    for r in result:
        print(f"    • {r['name']} → {r['movie_count']} movies")


#find relationships by conditions

def task5_find_relationships(session):
    
    

    # 1-High-intensity confrontations
    print("\n  [5a] High/extreme intensity confrontations:")
    result = session.run("""
        MATCH (c1:Character)-[r:INTERACTS_WITH]->(c2:Character)
        WHERE r.type = 'confrontation' AND r.intensity IN ['high', 'extreme']
        RETURN c1.name AS from, c2.name AS to, r.scenes AS scenes, r.intensity AS intensity
        ORDER BY r.scenes DESC
    """)
    for r in result:
        print(f"    • {r['from']} → {r['to']}  |  scenes: {r['scenes']}  |  intensity: {r['intensity']}")

    # 2-All alliances
    print("\n  [5b] Alliance relationships:")
    result = session.run("""
        MATCH (c1:Character)-[r:INTERACTS_WITH {type: 'alliance'}]->(c2:Character)
        RETURN c1.name AS from, c2.name AS to, r.scenes AS scenes
        ORDER BY r.scenes DESC
    """)
    for r in result:
        print(f"    • {r['from']} → {r['to']}  |  scenes: {r['scenes']}")

    # 3-Characters who appear in 'The Dark Knight' and how they interact
    print("\n  [5c] Interactions among 'The Dark Knight' cast:")
    result = session.run("""
        MATCH (c1:Character)-[:APPEARS_IN]->(m:Movie {title: 'The Dark Knight'}),
              (c2:Character)-[:APPEARS_IN]->(m),
              (c1)-[r:INTERACTS_WITH]->(c2)
        RETURN c1.name AS from, c2.name AS to, r.type AS type, r.scenes AS scenes
        ORDER BY r.scenes DESC
    """)
    for r in result:
        print(f"    • {r['from']} → {r['to']}  |  type: {r['type']}  |  scenes: {r['scenes']}")

    # 4-Full path: Actor → played Character → interacts with Character → played by Actor
    print("\n  [5d] Actor–Character interaction paths (actor A's char interacts with actor B's char):")
    result = session.run("""
        MATCH (a1:Actor)<-[:PLAYED_BY]-(c1:Character)-[r:INTERACTS_WITH]->(c2:Character)-[:PLAYED_BY]->(a2:Actor)
        RETURN a1.name AS actor1, c1.name AS char1,
               r.type AS rel_type,
               c2.name AS char2, a2.name AS actor2
        ORDER BY a1.name
    """)
    for r in result:
        print(f"    • {r['actor1']} ({r['char1']})  --[{r['rel_type']}]-->  {r['char2']} ({r['actor2']})")


#main

def main():
   
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    wait_for_neo4j(driver)

    with driver.session() as session:
        # Clean slate for re-runs
        session.run("MATCH (n) DETACH DELETE n")

        task1_create(session)
        task2_delete(session)
        task3_update(session)
        task4_find_nodes(session)
        task5_find_relationships(session)

    driver.close()
    print("\nDone. Open http://localhost:7474 cmd to explore the graph visually.\n")


if __name__ == "__main__":
    main()
