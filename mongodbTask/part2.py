from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydb = client["Company_db"]

# Drop all collections
mydb["Departments"].drop()
mydb["Employees"].drop()
mydb["Projects"].drop()

col1 = mydb["Departments"]
col1.insert_many([
    {"_id": 1, "name": "Engineering", "location": "Cairo"},
    {"_id": 2, "name": "Marketing",   "location": "Alexandria"},
    {"_id": 3, "name": "HR",          "location": "Giza"},
])


col2 = mydb["Projects"]
col2.insert_many([
    {"_id": 1, "title": "Website Redesign", "budget": 50000},
    {"_id": 2, "title": "Mobile App",       "budget": 80000},
    {"_id": 3, "title": "HR System",        "budget": 30000},
])

col3 = mydb["Employees"]
col3.insert_many([
    {"_id": 1, "name": "Ali",    "role": "Developer", "department_id": 1, "project_ids": [1, 2]},
    {"_id": 2, "name": "Sara",   "role": "Designer",  "department_id": 1, "project_ids": [2]},
    {"_id": 3, "name": "Mona",   "role": "Manager",   "department_id": 2, "project_ids": [3]},
    {"_id": 4, "name": "Omar",   "role": "Assistant", "department_id": 3, "project_ids": [1, 3]},
    {"_id": 5, "name": "Mariam", "role": "Analyst",   "department_id": 1, "project_ids": [1, 2, 3]},
])

print("Documents inserted successfully.")
print("Employees sample:", col3.find_one())
print("Projects sample:", col2.find_one())


# CMD SCRIPT:
"""
1—   docker exec -it mongodbTask python3 /mis-project/mongodbTask/part2.py
2-   docker exec -it mongodbTask mongosh
3-   use Company_db
4-   Agg1:-   
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
                
5-  Agg2:-
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
"""