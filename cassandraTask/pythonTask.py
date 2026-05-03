from cassandra.cluster import Cluster
import uuid
from datetime import datetime

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute(
    "CREATE KEYSPACE IF NOT EXISTS task WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}"
)
session.set_keyspace('task')

# ─────────────────────────────────────────────
# Create fresh students table
# studentId : primary key (int, auto-assigned)
# createdAt : clustering key (DESC)
# id        : original uuid preserved as column
# ─────────────────────────────────────────────
session.execute(
    """
    CREATE TABLE IF NOT EXISTS students
    (
        studentId    int,
        createdAt    timestamp,
        id           uuid,
        gpa          float,
        email        varchar,
        student_name varchar,
        PRIMARY KEY (studentId, createdAt)
    ) WITH CLUSTERING ORDER BY (createdAt DESC)
    """
)
print("Table created successfully")

insert_query = session.prepare(
    """
    INSERT INTO students (studentId, createdAt, id, gpa, email, student_name)
    VALUES (?, ?, ?, ?, ?, ?)
    """
)

uu     = uuid.uuid4()
uudate = datetime.now()

rows = [
    (1, datetime.now(), uuid.uuid4(), 3.5, 'john@gmail.com',    'John'),
    (2, datetime.now(), uuid.uuid4(), 3.5, 'jane@gmail.com',    'Jane'),
    (3, datetime.now(), uuid.uuid4(), 3.8, 'bob@gmail.com',     'Bob'),
    (4, datetime.now(), uuid.uuid4(), 3.9, 'alice@gmail.com',   'Alice'),
    (5, uudate,         uu,           3.5, 'charlie@gmail.com', 'Charlie'),
]

for row in rows:
    session.execute(insert_query, row)
print("Data inserted successfully")


def print_data(message, result_set):
    print(f"\n--- {message} ---")
    for row in result_set:
        print(row)


res = session.execute("SELECT * FROM students")
print_data("After Initial Insert", res)

# Update Charlie's GPA
session.execute(
    "UPDATE students SET gpa = 4.0 WHERE studentId = %s AND createdAt = %s",
    (5, uudate)
)

res = session.execute("SELECT * FROM students")
print_data("After Updating Charlie's GPA", res)

# Delete Charlie
session.execute(
    "DELETE FROM students WHERE studentId = %s AND createdAt = %s",
    (5, uudate)
)

res = session.execute("SELECT * FROM students")
print_data("After Deleting Charlie", res)
