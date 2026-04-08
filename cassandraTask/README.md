# Cassandra Python Task

This project demonstrates basic Cassandra CRUD operations using Python and the DataStax Cassandra driver.

## Requirements

- Python 3.13+
- Apache Cassandra running locally on `127.0.0.1:9042`

## Dependencies

Installed dependencies:

- `pyasyncore`
- `cassandra-driver`

## Setup

If you are using the included virtual environment in this project:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install dependencies:

```powershell
pip install pyasyncore
pip install cassandra-driver
```

## Run

From the project root:

```powershell
python pythonTask.py
```

## What the script does

The script in `pythonTask.py`:

- connects to local Cassandra cluster
- creates keyspace `task` if it does not exist
- creates table `students` if it does not exist
- inserts sample student rows
- updates one student GPA
- deletes one student row
- prints table contents after each operation

## Verified Status

The script was executed successfully in this workspace using:

```powershell
c:/Users/mahmo/OneDrive/Desktop/study/Uni/MIs/project/cassandraTask/.venv/Scripts/python.exe pythonTask.py
```

Output confirms:

- table creation
- data insertion
- update operation
- delete operation

## Notes

- Running the script multiple times will keep adding new sample rows because new UUIDs are generated on each run.
