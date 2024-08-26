import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to the database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Define user credentials
username = 'admin'
password = 'admin123'

# Delete the existing user
c.execute("DELETE FROM users WHERE username = ?", (username,))
conn.commit()
print(f"User '{username}' deleted successfully.")

# Insert the user again
hashed_password = hash_password(password)
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
conn.commit()
print("User re-added successfully!")

# Close the connection
conn.close()
