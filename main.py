import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os
import pathlib
import sys
from config import config
from commands import create_tables as create_tables_commands
from src.init_database import init_database
from src.create_main_interface import create_main_interface
from ui.categories import CategoryManagement


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Initialize database
        self.conn, self.cursor = init_database()

        self.main_frame = tk.Frame(root, bg='#f0f0f0')

        self.category_management = CategoryManagement(
            self.root, self.main_frame, self.cursor, self.conn)

        # Create main interface
        create_main_interface(
            self.root, self.main_frame, self.category_management.show_categories)


def main():
    root = tk.Tk()
    InventoryManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
