import mysql.connector
from database_config import db_config

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50),
            password VARCHAR(50)
        )
    """)

    # Clear old data and add prateek
    cursor.execute("TRUNCATE TABLE users")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', '3x9!ls#2')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('prateek', 'root')") 
    
    conn.commit()
    print("✅ SUCCESS: 'users' table created and 'prateek' added.")
    conn.close()
except Exception as e:
    print(f"❌ DATABASE ERROR: {e}")