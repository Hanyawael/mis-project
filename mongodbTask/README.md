# MIS Project - MongoDB Task

## Setup
- MongoDB running in Docker container named `mongodbTask`
- Python 3 installed inside the container
- Volume mounted from local machine to container

## How to Run

### Start the container
```bash
docker start mongodbTask
```

### Run Part 1
```bash
docker exec -it mongodbTask python3 /mis-project/mongodbTask/part1.py
```

### Run Part 2
```bash
docker exec -it mongodbTask python3 /mis-project/mongodbTask/part2.py
```

---

## Part 1 — Collections & Operations (school_db)

### Collections
- `students` — contains student documents
- `courses` — contains course documents

### Operations
1. Created 3 documents in each collection
2. Deleted 1 document from each collection (_id: 3)
3. Added `Score` array to 2 documents in each collection
4. Updated Score array conditionally:
   - `_id = 1` → put 5 in position [2]
   - `_id != 1` → put 6 in position [3]
5. Multiplied every element in Score array by 20 using `$map`

---

## Part 2 — Relationships & Aggregation (Company_db)

### Collections
- `Departments` — 3 departments (one side)
- `Employees` — 5 employees, each references a department (many side)
- `Projects` — 3 projects, referenced by employees via `project_ids` array

### Relationships
- **Departments → Employees**: one-to-many (employee stores `department_id`)
- **Employees → Projects**: one-to-many (employee stores `project_ids` array)

### Aggregation in CMD

#### Open mongosh
```bash
docker exec -it mongodbTask mongosh
```

#### Switch to database
```js
use Company_db
```

#### Aggregation 1 — Employee with their Department
```js
db.Employees.aggregate([
  {
    $lookup: {
      from: "Departments",
      localField: "department_id",
      foreignField: "_id",
      as: "department_info"
    }
  },
  { $unwind: "$department_info" },
  {
    $project: {
      name: 1,
      role: 1,
      "department_info.name": 1,
      "department_info.location": 1
    }
  }
])
```

#### Aggregation 2 — Employee with Department and Projects combined
```js
db.Employees.aggregate([
  {
    $lookup: {
      from: "Departments",
      localField: "department_id",
      foreignField: "_id",
      as: "department_info"
    }
  },
  { $unwind: "$department_info" },
  {
    $lookup: {
      from: "Projects",
      localField: "project_ids",
      foreignField: "_id",
      as: "projects_info"
    }
  },
  {
    $project: {
      name: 1,
      role: 1,
      "department_info.name": 1,
      "department_info.location": 1,
      "projects_info.title": 1,
      "projects_info.budget": 1
    }
  }
])
```