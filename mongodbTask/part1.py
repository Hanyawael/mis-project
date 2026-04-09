from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["mydb"]

students = db["students"]
courses = db["courses"]

students.delete_many({})
courses.delete_many({})

1-Create collections

students.insert_many([
    {"_id": 1, "name": "Ahmed"},
    {"_id": 2, "name": "Ali"},
    {"_id": 3, "name": "Sara"},
    {"_id": 4, "name": "Mona"},
    {"_id": 5, "name": "Omar"},
    {"_id": 6, "name": "Yara"},
    {"_id": 7, "name": "Khaled"}
])

courses.insert_many([
    {"_id": 1, "title": "Math"},
    {"_id": 2, "title": "Physics"},
    {"_id": 3, "title": "CS"},
    {"_id": 4, "title": "AI"},
    {"_id": 5, "title": "DB"},
    {"_id": 6, "title": "Networks"},
    {"_id": 7, "title": "Security"}
])

2-delete documents from each collection

students.delete_many({"_id": {"$in": [5, 6, 7]}})
courses.delete_many({"_id": {"$in": [5, 6, 7]}})

3-Update documents [add an array called ‘Score’] in each collection.

students.update_many(
    {"_id": {"$in": [1, 2, 3, 4]}},
    {"$set": {"Score": [1, 2, 3]}}
)

courses.update_many(
    {"_id": {"$in": [1, 2, 3, 4]}},
    {"$set": {"Score": [2, 3, 4]}}
)

4-If the ‘_id’ of the document =1 update the array called ‘Score’
and put number 5 in the third position of the array, if not  put
number 6 in the fourth position. 

students.update_many(
    {"_id": 1},
    {"$set": {"Score.2": 5}}
)

courses.update_many(
    {"_id": 1},
    {"$set": {"Score.2": 5}}
)

students.update_many(
    {"_id": {"$ne": 1}},
    {"$set": {"Score.3": 6}}
)

courses.update_many(
    {"_id": {"$ne": 1}},
    {"$set": {"Score.3": 6}}
)


5-Multiply each element in the array called ‘Score’ by 20.
for doc in students.find({"Score": {"$exists": True}}):
    new_score = [x * 20 for x in doc["Score"]]
    students.update_one(
        {"_id": doc["_id"]},
        {"$set": {"Score": new_score}}
    )

for doc in courses.find({"Score": {"$exists": True}}):
    new_score = [x * 20 for x in doc["Score"]]
    courses.update_one(
        {"_id": doc["_id"]},
        {"$set": {"Score": new_score}}
    )
