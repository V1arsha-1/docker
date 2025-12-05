import psycopg2
import time

time.sleep(5)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="newdb",
        user="user",
        password="pass"
    )
    print("Connected to the database!")
    conn.close()

except Exception as e:
    print("Connection failed:", e)
