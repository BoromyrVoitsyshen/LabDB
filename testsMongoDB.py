from pymongo import MongoClient
from datetime import datetime, timedelta
import time

client = MongoClient("mongodb+srv://user1:ZwSdByjWHjTuvjRZ@lab2.n8fdl.mongodb.net/")
db = client['Lab2']

def test_mongo_insert():
    reviews = []
    for i in range(10000): 
        review = {
            "_id": f"review_{i}",
            "title": f"Review Title {i}",
            "text": f"This is a sample text for review {i}.",
            "rating": round(3 + (i % 3) * 0.5, 1),  
            "user_name": f"user_{i}",
            "user_id": i % 500,
            "ware_id": i % 500, 
            "is_deleted": False,
            "last_modify_date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "comments": [
                {
                    "comment_id": f"comment_{i}_1",
                    "text": f"This is the first comment for review {i}.",
                    "date": (datetime.now() - timedelta(days=i, hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "likes": i * 2,
                    "dislikes": i % 2,
                    "user_name": f"comment_user_{i}_1",
                    "user_id": 2000 + i
                },
                {
                    "comment_id": f"comment_{i}_2",
                    "text": f"This is the second comment for review {i}.",
                    "date": (datetime.now() - timedelta(days=i, hours=2)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "likes": i * 3,
                    "dislikes": i % 3,
                    "user_name": f"comment_user_{i}_2",
                    "user_id": 3000 + i
                }
            ]
        }
        reviews.append(review)

    start_time = time.time()
    db.Reviews.insert_many(reviews)
    end_time = time.time()

    print(f"MongoDB Insert Time: {end_time - start_time} seconds")

def test_mongo_delete():
    start_time = time.time()
    result = db.Reviews.delete_many({"is_deleted": False}) 
    end_time = time.time()

    print(f"MongoDB Delete Time: {end_time - start_time} seconds")

def test_mongo_query():
    start_time = time.time()
    reviews = list(db.Reviews.find({"rating": {"$gte": 4}}))
    end_time = time.time()

    print(f"MongoDB Query Time: {end_time - start_time} seconds")

def test_mongo_update():
    start_time = time.time()
    result = db.Reviews.update_many(
        {}, 
        {"$set": {"last_modify_date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}}
    )
    end_time = time.time()

    print(f"MongoDB Update Time: {end_time - start_time} seconds")

test_mongo_delete()
test_mongo_insert()
test_mongo_query()
test_mongo_update()