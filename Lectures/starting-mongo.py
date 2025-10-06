# Here are all the necessary imports (which you might need)
from pymongo import MongoClient 

# Connect to your MongoDB Database by localhost connection (used during the lecture)
# Client == your MongoDB connection port, db == your database, users == collection
client = MongoClient("mongodb://localhost:27017")
db = client["ecommerce"]
users = db["users"]

# Create a function to insert information into your database, you can fill this with random information
def insert_user():
    users.insert_one({
        "user_ID": 1,
        "name": "Anna",
        "email": "anna@email.com",
        "orders": [{"product": "Phone", "price": 699}]
    })

# Create a function to get users who ordered a phone by orders.product category
all_users = users.find({"orders.product": "Phone"})

# Create a for loop function to print a name of all users after one another
for u in all_users:
    print(u["name"])
    

user = users.find_one({"user_ID": 1}, {"_id": 0, "name": 1, "email": 1})
print(user)

print("Hello!")
