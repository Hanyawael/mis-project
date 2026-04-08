# MIS Project - MongoDB Task

## Setup
- MongoDB running in Docker container named `mongodbTask`
- Python 3 installed inside the container

## How to run
1. Start the container:
   `docker start mongodbTask`

2. Enter the container:
   `docker exec -it mongodbTask bash`

3. Install dependencies (first time only):
   `pip3 install pymongo --break-system-packages`

4. Run the scripts:
   `python3 /mis-project/mongodbTask/part1.py`
   `python3 /mis-project/mongodbTask/part2.py`

## Notes
- Member A handles part1.py
- Member B handles part2.py
- Delete the test lines at the top of part1.py before starting