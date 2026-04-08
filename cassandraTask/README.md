# Cassandra Python Task (Dockerized)

This project demonstrates basic Cassandra CRUD operations using Python and the DataStax Cassandra driver, with Cassandra running in Docker.

## Requirements

- Docker Desktop (or Docker Engine)
- Python 3.10+

## 1) Start Cassandra in Docker

From the project root, run:

```powershell
docker run --name cassandra-task -p 9042:9042 -d cassandra:latest
```

Check that the container is running:

```powershell
docker ps
```

Wait until Cassandra is ready (first startup may take a minute):

```powershell
docker logs -f cassandra-task
```

Stop logs when you see Cassandra startup complete.

## 2) Install Python dependencies

If you use the included virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install required packages:

```powershell
pip install cassandra-driver
pip install pyasyncore
```

## 3) Run the script

```powershell
python pythonTask.py
```

The script connects to Cassandra at `127.0.0.1:9042`, which maps to the Docker container port.

## What the script does

The script in `pythonTask.py`:

- creates keyspace `task` if it does not exist
- creates table `students` if it does not exist
- inserts sample student rows
- updates one student GPA
- deletes one student row
- prints table contents after each operation

## Docker helper commands

Stop container:

```powershell
docker stop cassandra-task
```

Start existing container again:

```powershell
docker start cassandra-task
```

Remove container:

```powershell
docker rm -f cassandra-task
```

## Notes

- Running the script multiple times keeps adding new sample rows because new UUIDs are generated on each run.
- If connection fails, verify container health with `docker ps` and check logs with `docker logs cassandra-task`.
