from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://root:6DMoxqDLmJ@10.244.0.66:27017/')
db = client['shop_db']

# Insert Users
users = [
    {
        "userID": "user1",
        "userName": "Alice",
        "purchases": ["item1", "item3", "item5"]
    },
    {
        "userID": "user2",
        "userName": "Bob",
        "purchases": ["item2", "item4"]
    },
    {
        "userID": "user3",
        "userName": "Charlie",
        "purchases": ["item1", "item4", "item6"]
    },
    {
        "userID": "user4",
        "userName": "Diana",
        "purchases": ["item3", "item5"]
    },
    {
        "userID": "user5",
        "userName": "Eve",
        "purchases": ["item2", "item6"]
    }
]

db.users.insert_many(users)

# Insert Items
items = [
    {
        "id": "item1",
        "name": "Xbox",
        "price": 299.99
    },
    {
        "id": "item2",
        "name": "PlayStation",
        "price": 499.99
    },
    {
        "id": "item3",
        "name": "PC",
        "price": 999.99
    },
    {
        "id": "item4",
        "name": "Camera",
        "price": 199.99
    },
    {
        "id": "item5",
        "name": "Headphones",
        "price": 89.99
    },
    {
        "id": "item6",
        "name": "Smartphone",
        "price": 799.99
    }
]

db.items.insert_many(items)

print("Data inserted successfully!")
