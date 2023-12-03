import fake
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["student-finances"]
users_collection = db["users"]
transactions_collection = db["transactions"]

#TODO: pass in scraped data
names = ["bippis mippis", "ippis lippis", "joe rogan", "bim job"]

users = fake.fake_user_data(names)

users_collection.insert_many(users)

for u in users:
	t = fake.fake_user_transaction_data(u.get("user_id"))
	transactions_collection.insert_many(t)