import sqlite3

# Connect to the database
conn = sqlite3.connect('inventory.db')
c = conn.cursor()

# Fetch all users
c.execute("SELECT id, username FROM users")
users = c.fetchall()

print("Existing Users:")
for user in users:
    print(f"ID: {user[0]}, Username: {user[1]}")

# Close the connection
conn.close()
