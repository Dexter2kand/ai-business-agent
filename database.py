
import sqlite3

# Connect to database
conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

# Create customer table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# Insert sample data
customers = [
    ("1025", "John Smith", "Processing"),
    ("1026", "Anna Mueller", "Completed"),
    ("1027", "David Brown", "Pending")
]

cursor.executemany("""
INSERT OR IGNORE INTO customers (id, name, status)
VALUES (?, ?, ?)
""", customers)

conn.commit()

# Verify database
cursor.execute("SELECT * FROM customers")

print("Customer Database:")
for customer in cursor.fetchall():
    print(customer)

conn.close()

