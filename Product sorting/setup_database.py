import sqlite3
from werkzeug.security import generate_password_hash

# Create database and users table
connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
connection.commit()

# Add a sample user
username = "testuser"
password = "password123"
hashed_password = generate_password_hash(password)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
connection.commit()
connection.close()

print("Database setup complete!")
