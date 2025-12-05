#**DevOps Practice Project: Containerizing and Deploying a Python App with Docker**

Project Overview
This project demonstrates how to Install and set up Docker on your system.Use PostgreSQL inside a Docker container.Create and manage a database and tables.Dockerize a Python application to connect to PostgreSQL.Use Docker networks to allow containers to communicate.This is a beginner-friendly guide with clear steps, commands, and explanations.

System Requirements for this project

Docker Desktop
Windows 10/11 (64-bit, Pro/Enterprise/Education with WSL2 enabled)
macOS (Intel or Apple Silicon)
Linux (use your package manager: apt, dnf, etc.)
Download: Docker Desktop
VS Code (optional but recommended)
Download: VS Code
Recommended Extensions:
Docker by Microsoft
Remote - Containers (optional)

Step 1 — Verify Docker Installation

Open terminal and run:

docker --version
docker info
<img width="876" height="77" alt="image" src="https://github.com/user-attachments/assets/ae00a2f0-aac0-41b7-ad55-66f01b3c3aa9" />

Expected: Docker is installed and running.

Step 2 — Pull Required Images

Pull the base Python image:
docker pull python:3.11-slim
Pull PostgreSQL image:
docker pull postgres
<img width="1082" height="213" alt="image" src="https://github.com/user-attachments/assets/e5fd2cd2-fb39-473e-92a4-84ac9b8ca67d" />

Step 3 — Create a Docker Network
Create a custom network for container communication:
docker network create mynetwork1

Verify:

docker network ls
<img width="872" height="187" alt="image" src="https://github.com/user-attachments/assets/ae629afc-c5f1-4ab1-9b00-73cbda55f008" />
You should see mynetwork1 listed.

Step 4 — Run PostgreSQL Container
Run PostgreSQL on the custom network:

docker run -d \
  --name my-postgres \
  --network mynetwork1 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=pass \
  -e POSTGRES_DB=newdb \
  postgres


Explanation:

-d → Run container in detached mode.
--name my-postgres → Container name.
--network mynetwork1 → Connect to the custom network.
-e POSTGRES_USER, -e POSTGRES_PASSWORD, -e POSTGRES_DB → Environment variables to configure DB.
postgres → Image name.

Verify container is running:
docker ps
<img width="1318" height="112" alt="image" src="https://github.com/user-attachments/assets/69160072-e1a0-4e89-b27d-5b8f9c276f10" />

Step 5 — Enter PostgreSQL Container
To access PostgreSQL terminal:
docker exec -it my-postgres bash
Inside container, enter:
psql -U user -d newdb
You are now at the PostgreSQL prompt:
newdb=#

Step 6 — Create a Table
Create a Library Management table:

CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INT,
    genre TEXT,
    isbn TEXT UNIQUE,
    is_available BOOLEAN DEFAULT TRUE
);
![d1](https://github.com/user-attachments/assets/756fcefe-7782-43fb-8400-418483ee70cf)



SERIAL → Auto-increment integer (primary key).

BOOLEAN DEFAULT TRUE → Availability status.

UNIQUE → Ensures ISBN is unique.

Step 7 — Insert Sample Data
INSERT INTO books (title, author, published_year, genre, isbn)
VALUES 
('The Alchemist', 'Paulo Coelho', 1988, 'Fiction', '9780061122415'),
('Clean Code', 'Robert C. Martin', 2008, 'Programming', '9780132350884'),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997, 'Fantasy', '9780590353427');


Check inserted data:

SELECT * FROM books;

Step 8 — Create Python App

Create app.py in your project folder:

import psycopg2
import time

# Wait for PostgreSQL to start
time.sleep(5)

try:
    conn = psycopg2.connect(
        host="my-postgres",
        database="newdb",
        user="user",
        password="pass"
    )
    print("Connected to the database!")

    cur = conn.cursor()

    # Insert a sample row
    cur.execute("""
        INSERT INTO books (title, author, published_year, genre, isbn)
        VALUES ('Docker for Beginners', 'Varsha P', 2025, 'Tech', '9781234567890');
    """)
    conn.commit()
    print("Data inserted successfully!")

    # Fetch all rows
    cur.execute("SELECT * FROM books;")
    rows = cur.fetchall()
    print("Data in table:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()

except Exception as e:
    print("Connection failed:", e)

Step 9 — Create Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install psycopg2-binary
![d3](https://github.com/user-attachments/assets/8d23fe57-f820-44ce-a9d0-98c2c3abaf53)
CMD ["python", "app.py"]
WORKDIR /app → Set working directory.
COPY app.py . → Copy Python app into container.
RUN pip install psycopg2-binary → Install PostgreSQL driver.
CMD → Command to run when container starts.

Step 10 — Build Docker Image
docker build --no-cache -t my-python-app .
--no-cache → Forces Docker to rebuild the image with latest code.
<img width="1315" height="271" alt="image" src="https://github.com/user-attachments/assets/f2222ca4-148c-4f42-9990-74f7796dabca" />

Step 11 — Run Python Container
docker run --rm --network mynetwork1 my-python-app
Expected Output:
![d4](https://github.com/user-attachments/assets/c3c42b18-925f-45bb-aff8-1a176a453aff)
Connected to the database!

Data inserted successfully!

Data in table:
(1, 'The Alchemist', 'Paulo Coelho', 1988, 'Fiction', '9780061122415', True)
(2, 'Clean Code', 'Robert C. Martin', 2008, 'Programming', '9780132350884', True)
(3, 'Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', 1997, 'Fantasy', '9780590353427', True)
(4, 'Docker for Beginners', 'Varsha P', 2025, 'Tech', '9781234567890', True)

Step 12 — Cleanup (Optional)
Stop and remove containers/images:
docker stop my-postgres
docker rm my-postgres
docker rmi my-python-app
docker network rm mynetwork1

Step 13 — Extra Practice Ideas
Update availability:
UPDATE books SET is_available = FALSE WHERE book_id = 2;
Delete a book:
DELETE FROM books WHERE book_id = 3;
Filter by genre:
SELECT * FROM books WHERE genre = 'Programming';
Add more tables (e.g., members, loans) and link them with foreign keys.



