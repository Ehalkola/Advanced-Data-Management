# Here are all the necessary imports (which you might need)
from pymongo import MongoClient 

# Connect to your MongoDB Database by localhost connection (used during the lecture)
# Client == your MongoDB connection port, db == your database, users == collection
client = MongoClient("mongodb://localhost:27017")
db = client["my_hoteldb"]
hotels = db["hotels"]


# Task set 1: Insert at least 3 different hotels into hotel collection
# do this according to instructions
# Create some data about hotels according to instructions -->
# Insert these into the collection
hotel_data = [
    {
        "hotelId": 1,
        "name": "Grand Hotel",
        "location": "Helsinki",
        "facilities": ["wifi", "pool", "gym"],
        "reviews": [
            {"user": "David", "rating": 5, "comment": "Excellent service!"},
            {"user": "Bob", "rating": 4, "comment": "Nice location, near city centre!"}
        ]
    },
    {
        "hotelId": 2,
        "name": "Glass Resort",
        "location": "Rovaniemi",
        "facilities": ["wifi", "spa", "ala carte restaurant"],
        "reviews": [
            {"user": "John", "rating": 5, "comment": "Beautiful facilities and location!"}
        ]
    },
    {
        "hotelId": 3,
        "name": "Santa's Hotel Santa Claus",
        "location": "Rovaniemi",
        "facilities": ["gym", "restaurant", "wifi"],
        "reviews": [
            {"user": "Eemil", "rating": 4, "comment": "Good service!"}
        ]
    }
]

# Insert above data into the collection
hotels.insert_many(hotel_data)

# Task 2:
# 2.1 Find all hotels in Helsinki
# You can use for loop for these first 2 to find hotels you are looking for
for helsinki_hotels in hotels.find({"location": "Helsinki"}):
    # Display the hotels in Helsinki for the user
    print(helsinki_hotels)

# 2.2 Find all hotels that have “pool”
for pool_hotels in hotels.find({"facilities": "pool"}):
    # Display the hotels with pools to the user
    print(pool_hotels)

# 2.3 Find the first hotel that has a rating of 5 in any review
# This one can be done without for loop
five_star_hotels = hotels.find_one({"reviews.rating": 5})
# Display the 5 star hotels to the user
print(five_star_hotels)

# Task set 3:
# Task 3.1: # 1. Add 'spa' facility to Grand Hotel
hotels.update_one(
    {"name": "Grand Hotel"},
    {"$addToSet": {"facilities": "spa"}}  # addToSet avoids duplicates
)

# 3.2 Update Bob’s review in Grand Hotel to rating 5
hotels.update_one(
    {"name": "Grand Hotel", "reviews.user": "Bob"},
    {"$set": {"reviews.$.rating": 5}}
)

# 3.3 Add new review for Carol with rating 3
hotels.update_one(
    {"name": "Grand Hotel"},
    {"$push": {"reviews": {"user": "Carol", "rating": 3, "comment": "Service is good, but restaurant could be better."}}}
)

# Task set 4:
# 4.1 Delete all hotels that don’t have wifi
hotels.delete_many({"facilities": {"$ne": "wifi"}})

# 4.2 Delete all reviews by Carol
hotels.update_many(
    {},
    {"$pull": {"reviews": {"user": "Carol"}}}
)

# Task set 5:
# 5.1 Show the average rating for each hotel
pipeline1 = [
    {"$unwind": "$reviews"},
    {"$group": {"_id": "$name", "avg_rating": {"$avg": "$reviews.rating"}}}
]
for doc in hotels.aggregate(pipeline1):
    print(doc)

# 5.2 Find top 2 hotels by average rating
pipeline2 = [
    {"$unwind": "$reviews"},
    {"$group": {"_id": "$name", "avg_rating": {"$avg": "$reviews.rating"}}},
    {"$sort": {"avg_rating": -1}},
    {"$limit": 2}
]
for doc in hotels.aggregate(pipeline2):
    print(doc)

# 5.3 Count how many hotels offer gym
count = hotels.count_documents({"facilities": "gym"})
print("Hotels with gym:", count)