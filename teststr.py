import sqlite3
import json

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
user_data = [{"name": "John Doe", "age": 30},
             {"name": "Jane Doe", "age": 25}]

for user in user_data:
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (user["name"], user["age"]))

conn.commit()
cursor.execute("SELECT * FROM users")
