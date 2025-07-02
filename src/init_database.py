import sqlite3
import os
import pathlib
import sys


DB_FILE_NAME = 'inventory.db'

CREATE_CATEGORIES_TABLE = '''
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)'''

CREATE_ITEMS_TABLE = '''
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    serial_no TEXT UNIQUE NOT NULL,
    category_id TEXT,
    total_amount INTEGER NOT NULL,
    available_amount INTEGER NOT NULL,
    price REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
)'''

CREATE_CUSTOMERS_TABLE = '''
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mobile TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

# Create purchases table
CREATE_PURCHASES_TABLE = '''
CREATE TABLE IF NOT EXISTS purchases (
    id TEXT PRIMARY KEY,
    customer_id TEXT,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
)
'''

# Create purchase_items table
CREATE_PURCHASE_ITEMS_TABLE = '''
CREATE TABLE IF NOT EXISTS purchase_items (
    id TEXT PRIMARY KEY,
    purchase_id TEXT,
    item_id TEXT,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchases (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
)
'''


def init_database():
    try:
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(os.path.join(pathlib.Path(
            __file__).resolve().parent.parent, 'db', DB_FILE_NAME))
        cursor = conn.cursor()

        if (cursor is None):
            raise Exception("Database connection failed")

        # Create categories table
        cursor.execute(CREATE_CATEGORIES_TABLE)

        # Create items table
        cursor.execute(CREATE_ITEMS_TABLE)

        # Create customers table
        cursor.execute(CREATE_CUSTOMERS_TABLE)

        # Create purchases table
        cursor.execute(CREATE_PURCHASES_TABLE)

        # Create purchase_items table
        cursor.execute(CREATE_PURCHASE_ITEMS_TABLE)

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        sys.exit(1)
