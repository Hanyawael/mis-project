from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
#Testing purposes -DELETE THIS
db = client["school_db"]
db.test.drop()
db.test.insert_one({"message": "connection works!"})
doc = db.test.find_one()
print(doc)
print("MongoDB connection is working. Delete these lines and start your work.")