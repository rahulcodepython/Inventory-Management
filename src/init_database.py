import os
import pathlib
import sys
import sqlite3
from config import config
from commands import create_tables as create_tables_commands
from src.resources_path import resource_path


def init_database():
    """Initialize SQLite database and return connection and cursor"""
    try:
        db_path = resource_path(os.path.join("db", config.DB_FILE_NAME))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if cursor is None:
            raise Exception("Database connection failed")

        # Create all tables
        cursor.execute(create_tables_commands.CREATE_CATEGORIES_TABLE)
        cursor.execute(create_tables_commands.CREATE_ITEMS_TABLE)
        cursor.execute(create_tables_commands.CREATE_CUSTOMERS_TABLE)
        cursor.execute(create_tables_commands.CREATE_PURCHASES_TABLE)
        cursor.execute(create_tables_commands.CREATE_PURCHASE_ITEMS_TABLE)

        conn.commit()
        return conn, cursor

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        sys.exit(1)
