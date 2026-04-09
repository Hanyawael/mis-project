# Neo4j Python Task (Dockerized)

This project demonstrates basic Neo4j graph database operations using Python and the official Neo4j driver, with Neo4j and the app running together via Docker Compose.

The dataset models the **Batman Trilogy** as a character interaction graph — with Movies, Actors, and Characters as nodes, and relationships like `APPEARS_IN`, `PLAYED_BY`, and `INTERACTS_WITH`.

---

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Docker Compose)
- No local Python installation needed — everything runs inside Docker

---

## 1) Clone the repo

```bash
git clone https://github.com/Hanyawael/neo4jtask.git
cd neo4jtask
```

---

## 2) Start the containers

From the project root, run:

```bash
docker compose up --build
```

This will:
- Pull and start a **Neo4j 5.18** container with APOC plugins enabled
- Build and run the **Python app** container
- Wait for Neo4j to be healthy before running the script

> First startup may take a minute while Neo4j initializes.

To run in detached mode (background):

```bash
docker compose up --build -d
```

Then view the app logs with:

```bash
docker logs movie_app
```

---

## 3) View the graph visually

Once the containers are running, open the Neo4j Browser at:

```
http://localhost:7474
```

Login credentials:
- **Username:** `neo4j`
- **Password:** `password123`

Run this in the browser to see the full graph:

```cypher
MATCH (n)-[r]->(m) RETURN n, r, m
```

---

## What the script does

The script in `main.py` runs five tasks against the Neo4j database:

| Task | Description |
|------|-------------|
| **Task 1 – Create** | Creates Movie, Actor, and Character nodes with `APPEARS_IN`, `PLAYED_BY`, and `INTERACTS_WITH` relationships |
| **Task 2 – Delete** | Removes a property from Harvey Dent, deletes a relationship, then deletes the node entirely |
| **Task 3 – Update** | Updates Bruce Wayne's properties, modifies a relationship's intensity, and adds rating/box office data to a movie |
| **Task 4 – Find nodes** | Queries villain characters, post-2006 movies, British actors, and multi-movie characters |
| **Task 5 – Find relationships** | Queries high-intensity confrontations, alliances, cast interactions, and full actor→character paths |

---

## Docker helper commands

Stop all containers:

```bash
docker compose down
```

Stop and remove volumes (wipes Neo4j data):

```bash
docker compose down -v
```

Restart without rebuilding:

```bash
docker compose up
```

Rebuild after code changes:

```bash
docker compose up --build
```

View Neo4j logs:

```bash
docker logs movie_neo4j
```

---

