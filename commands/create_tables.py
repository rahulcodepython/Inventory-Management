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

CREATE_PURCHASES_TABLE = '''
CREATE TABLE IF NOT EXISTS purchases (
    id TEXT PRIMARY KEY,
    customer_id TEXT,
    purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
)
'''

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
