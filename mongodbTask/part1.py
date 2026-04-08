from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["mydb"]

students = db["students"]
courses = db["courses"]

print("Connected to MongoDB")

#1 Create two collections and create at least three documents in each one:
students.insert_many([
    {"_id": 1, "name": "Ahmed"},
    {"_id": 2, "name": "Ali"},
    {"_id": 3, "name": "Sara"}
])

courses.insert_many([
    {"_id": 1, "title": "Math"},
    {"_id": 2, "title": "Physics"},
    {"_id": 3, "title": "CS"}
])

#2 Delete at least one document from each collection:
students.delete_one({"_id": 3})
courses.delete_one({"_id": 3})

#3 Update at least two documents [add an array called ‘Score’] in each collection:
students.update_many(
    {"_id": {"$in": [1, 2]}},
    {"$set": {"Score": [1, 2, 3]}}
)

courses.update_many(
    {"_id": {"$in": [1, 2]}},
    {"$set": {"Score": [2, 3, 4]}}
)

#4 If the ‘_id’ of the document =1 update the array called ‘Score’ and put number 5 in the third position of the array, if not  put number 6 in the fourth position:
students.update_one(
    {"_id": 1},
    {"$set": {"Score.2": 5}}
)

courses.update_one(
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

#5 Multiply each element in the array called ‘Score’ by 20:
students.update_many(
    {},
    [{
        "$set": {
            "Score": {
                "$map": {
                    "input": "$Score",
                    "as": "s",
                    "in": {"$multiply": ["$$s", 20]}
                }
            }
        }
    }]
)

courses.update_many(
    {},
    [{
        "$set": {
            "Score": {
                "$map": {
                    "input": "$Score",
                    "as": "s",
                    "in": {"$multiply": ["$$s", 20]}
                }
            }
        }
    }]
)
