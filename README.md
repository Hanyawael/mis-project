# MIS Project — NoSQL Database Tasks

This repository contains three independent tasks covering **MongoDB**, **Apache Cassandra**, and **Neo4j**, each implemented in Python with Docker-based setup instructions.

---

## Repository Structure

```
mis-project/
├── mongodbTask/
│   ├── part1.py          # CRUD operations on two collections
│   ├── part2.py          # One-to-many relationships + aggregation
│   └── README.md
├── cassandraTask/
│   ├── pythonTask.py     # Table creation, insert, update, delete
│   ├── part2             # Shell commands: descending select + materialized view
│   └── README.md
└── neo4jtask/
    ├── main.py           # Full graph CRUD — Batman Trilogy dataset
    ├── requirements.txt
    └── README.md
```

---

## Task 1 — MongoDB

**Dataset:** `school_db` (Part 1) and `Company_db` (Part 2)

### What it covers

**Part 1 (`part1.py`)**
- Creates two collections: `students` and `courses`
- Deletes documents from each collection
- Adds a `Score` array to documents via `update_many`
- Conditionally updates Score positions: index `[2] = 5` when `_id == 1`, index `[3] = 6` otherwise
- Multiplies every element in Score by 20

**Part 2 (`part2.py`)**
- Creates a one-to-many relationship: `Departments → Employees → Projects`
- Demonstrates two aggregation pipelines using `$lookup`, `$unwind`, and `$project` in `mongosh`

### Prerequisites

- Docker Desktop installed and running
- A running MongoDB container named `mongodbTask` with the project directory mounted

### Running

```bash
# Start the container
docker start mongodbTask

# Run Part 1
docker exec -it mongodbTask python3 /mis-project/mongodbTask/part1.py

# Run Part 2
docker exec -it mongodbTask python3 /mis-project/mongodbTask/part2.py
```

### Aggregation (Part 2 — run in mongosh)

```bash
docker exec -it mongodbTask mongosh
```

```js
use Company_db

// Employees joined with their Department
db.Employees.aggregate([
  { $lookup: { from: "Departments", localField: "department_id", foreignField: "_id", as: "department_info" } },
  { $unwind: "$department_info" },
  { $project: { name: 1, role: 1, "department_info.name": 1, "department_info.location": 1 } }
])

// Employees joined with Department AND Projects
db.Employees.aggregate([
  { $lookup: { from: "Departments", localField: "department_id", foreignField: "_id", as: "department_info" } },
  { $unwind: "$department_info" },
  { $lookup: { from: "Projects", localField: "project_ids", foreignField: "_id", as: "projects_info" } },
  { $project: { name: 1, role: 1, "department_info.name": 1, "department_info.location": 1, "projects_info.title": 1, "projects_info.budget": 1 } }
])
```

---

## Task 2 — Apache Cassandra

**Dataset:** `task` keyspace, `students` table

### What it covers

**Part 1 (`pythonTask.py`)**
- Creates a keyspace and a `students` table with a composite primary key (`id` partition key + `createdAt` clustering key)
- Inserts 5 rows
- Updates one student's GPA
- Deletes one student row
- Prints table state after each operation

**Part 2 (shell — `part2` file)**
- Selects rows in descending order by clustering key using `cqlsh`
- Creates a materialized view (`students_by_email`) to query by a non-primary-key column

### Prerequisites

- Docker Desktop installed and running
- Python 3.10+
- `cassandra-driver` Python package

### Running

```bash
# Start Cassandra in Docker (first time)
docker run --name cassandra-task -p 9042:9042 -d \
  -e CASSANDRA_BROADCAST_RPC_ADDRESS=127.0.0.1 cassandra:latest

# Wait ~60 seconds for Cassandra to initialise, then:
docker ps

# If the container already exists from a previous run:
docker start cassandra-task

# Install Python dependency
pip install cassandra-driver

# Run Part 1
python cassandraTask/pythonTask.py
```

### Part 2 — Shell commands

```bash
# Enable materialized views (required once)
docker exec -it cassandra-task bash -c \
  "sed -i 's/materialized_views_enabled: false/materialized_views_enabled: true/' /etc/cassandra/cassandra.yaml"
docker restart cassandra-task
# Wait ~60 seconds again

# Open cqlsh
docker exec -it cassandra-task cqlsh
```

```sql
USE task;

-- Select rows in descending order (copy any id from Part 1 output)
SELECT * FROM students WHERE id = <paste-uuid-here> ORDER BY createdAt DESC;

-- Create materialized view on email (non-primary-key attribute)
CREATE MATERIALIZED VIEW students_by_email AS
  SELECT * FROM students
  WHERE email IS NOT NULL AND id IS NOT NULL AND createdAt IS NOT NULL
  PRIMARY KEY (email, id, createdAt);

-- Query the view
SELECT * FROM students_by_email;
```

---

## Task 3 — Neo4j

**Dataset:** Batman Trilogy — character interaction graph

**Nodes:** `Movie`, `Actor`, `Character`

**Relationships:** `APPEARS_IN`, `PLAYED_BY`, `INTERACTS_WITH` (with properties: scenes, type, intensity)

### What it covers

| Task | Description |
|------|-------------|
| **Create** | Movies, Actors, Characters nodes with all relationships and properties |
| **Delete** | Removes a property (`age`) from a node, deletes a relationship, then deletes a node entirely |
| **Update** | Updates node properties (Bruce Wayne's alias/status/age) and relationship properties (intensity, scenes) |
| **Find nodes** | Queries by role, year, nationality, and appearance count |
| **Find relationships** | Queries by interaction type, intensity, movie cast membership, and full actor→character paths |

### Prerequisites

- Docker Desktop installed and running
- Python 3.10+

```bash
pip install neo4j==5.18.0
```

### Running

```bash
# Start Neo4j in Docker
docker run --name neo4j-task -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 -d neo4j:5.18

# Wait ~30 seconds, then run the script
python neo4jtask/main.py
```

> **Note:** The script connects via Bolt on `bolt://localhost:7687`. Make sure your Neo4j container exposes port `7687`.

### Viewing the graph

Open the Neo4j Browser at `http://localhost:7474` and log in with `neo4j / password123`, then run:

```cypher
MATCH (n)-[r]->(m) RETURN n, r, m
```

