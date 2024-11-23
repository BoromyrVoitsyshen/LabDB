import pyodbc
import time
from datetime import datetime, timedelta

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=PAVILLIONGAMING\SQLEXPRESS;'
    'DATABASE=Lab2;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def test_sql_insert():
    start_time = time.time()
    comment_id = 1  

    for i in range(10000):  
        review_id = i + 1
        report_id = i + 1

        review_title = f"Review Title {i}"
        review_text = f"This is a review text for review {i}."
        review_rating = round(3 + (i % 3) * 0.5, 1)
        review_user_id = i % 500
        review_ware_id = i % 500
        review_is_deleted = 0
        review_last_modify_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO Review (Id, Title, Text, Rating, UserId, WareId, IsDeleted, LastModifyDate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, review_id, review_title, review_text, review_rating, review_user_id, review_ware_id, review_is_deleted, review_last_modify_date)

        for j in range(2):  
            comment_text = f"This is comment {j} for review {i}."
            comment_date = (datetime.now() - timedelta(days=i, hours=j)).strftime("%Y-%m-%d %H:%M:%S")
            comment_likes = i * 2 + j
            comment_dislikes = i % 2 + j
            comment_user_id = 2000 + i + j

            cursor.execute("""
                INSERT INTO Comment (Id, Text, Date, Likes, Dislikes, UserId, ReviewId)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, comment_id, comment_text, comment_date, comment_likes, comment_dislikes, comment_user_id, review_id)

            comment_id += 1  

        report_title = f"Report Title {i}"
        report_text = f"This is a report text for review {i}."
        report_date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        report_user_id = review_user_id

    conn.commit()
    end_time = time.time()
    print(f"SQL Insert Time: {end_time - start_time} seconds")

def test_sql_update():
    start_time = time.time()

    new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE Review
        SET LastModifyDate = ?;
    """, new_date)
    cursor.execute("""
        UPDATE Comment
        SET Date = ?;
    """, new_date)
    conn.commit()

    end_time = time.time()
    print(f"SQL Update Time: {end_time - start_time} seconds")

def test_sql_delete():
    start_time = time.time()

    cursor.execute("""
        DELETE Comment;
    """)
    cursor.execute("""
        DELETE Review;
    """)
    conn.commit()

    end_time = time.time()
    print(f"SQL DELETE Time: {end_time - start_time} seconds")

def test_sql_query():
    start_time = time.time()

    cursor.execute("SELECT * FROM Review WHERE Rating > 4;")
    cursor.execute("SELECT * FROM Comment WHERE Likes > 4;")
    rows = cursor.fetchall()
    for row in rows:
        pass  

    end_time = time.time()
    print(f"SQL Query Time: {end_time - start_time} seconds")

test_sql_delete()
test_sql_insert()
test_sql_update()
test_sql_query()

cursor.close()
conn.close()