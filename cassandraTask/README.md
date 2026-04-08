from cassandra.cluster import Cluster
import uuid
from datetime import datetime

cluster = Cluster(['127.0.0.1'])

session = cluster.connect()

session.execute(
    "CREATE KEYSPACE IF NOT EXISTS task WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}"
)

session.set_keyspace('task')

session.execute(
    """
    CREATE TABLE IF NOT EXISTS students
    (
        id uuid,
        createdAt timestamp,
        gpa float, 
        email varchar,
        student_name varchar,
        PRIMARY KEY (id, createdAt)
    ) WITH CLUSTERING ORDER BY (createdAt DESC)
    """
)
print("Table Created successfully")


insert_query = session.prepare(
    "INSERT INTO students (id, createdAt, gpa, email, student_name) VALUES (?, ?, ?, ?, ?)"
)


uu = uuid.uuid4()
uudate = datetime.now()

rows = [
    (uuid.uuid4(), datetime.now(), 3.5, 'john@gmail.com', 'John'),
    (uuid.uuid4(), datetime.now(), 3.5, 'jane@gmail.com', 'Jane'),
    (uuid.uuid4(), datetime.now(), 3.8, 'bob@gmail.com', 'Bob'),
    (uuid.uuid4(), datetime.now(), 3.9, 'alice@gmail.com', 'Alice'),
    (uu, uudate, 3.5, 'charlie@gmail.com', 'Charlie')
]



for row in rows:
    session.execute(insert_query, row)
print("Data Inserted successfully")


def print_data(message, result_set):
    print(f"\n--- {message} ---")
    for row in result_set:
        print(row)


res = session.execute("SELECT * FROM students")
print_data("After Initial Insert", res)

session.execute(
    "UPDATE students SET gpa = 4.0 WHERE id = %s AND createdAt = %s",
    (uu, uudate)
)

res = session.execute("SELECT * FROM students")
print_data("After Updating Charlie's GPA", res)

session.execute(
    "DELETE FROM students WHERE id = %s AND createdAt = %s",
    (uu, uudate)
)

res = session.execute("SELECT * FROM students")
print_data("After Deleting Charlie", res)
