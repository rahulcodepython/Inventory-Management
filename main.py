import tkinter as tk
from src.init_database import init_database
from tkinter import ttk, messagebox, filedialog
import sqlite3
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Initialize database
        init_database()

        # Create main interface
        self.create_main_interface()

    # def init_database(self):
    #     """Initialize SQLite database with required tables"""
    #     self.conn = sqlite3.connect('inventory.db')
    #     self.cursor = self.conn.cursor()

    #     # Create categories table
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS categories (
    #             id TEXT PRIMARY KEY,
    #             name TEXT UNIQUE NOT NULL,
    #             description TEXT,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         )
    #     ''')

    #     # Create items table
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS items (
    #             id TEXT PRIMARY KEY,
    #             name TEXT NOT NULL,
    #             serial_no TEXT UNIQUE NOT NULL,
    #             category_id TEXT,
    #             total_amount INTEGER NOT NULL,
    #             available_amount INTEGER NOT NULL,
    #             price REAL NOT NULL,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #             FOREIGN KEY (category_id) REFERENCES categories (id)
    #         )
    #     ''')

    #     # Create customers table
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS customers (
    #             id TEXT PRIMARY KEY,
    #             name TEXT NOT NULL,
    #             mobile TEXT UNIQUE NOT NULL,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    #         )
    #     ''')

    #     # Create purchases table
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS purchases (
    #             id TEXT PRIMARY KEY,
    #             customer_id TEXT,
    #             purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #             total_amount REAL NOT NULL,
    #             FOREIGN KEY (customer_id) REFERENCES customers (id)
    #         )
    #     ''')

    #     # Create purchase_items table
    #     self.cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS purchase_items (
    #             id TEXT PRIMARY KEY,
    #             purchase_id TEXT,
    #             item_id TEXT,
    #             quantity INTEGER NOT NULL,
    #             unit_price REAL NOT NULL,
    #             total_price REAL NOT NULL,
    #             FOREIGN KEY (purchase_id) REFERENCES purchases (id),
    #             FOREIGN KEY (item_id) REFERENCES items (id)
    #         )
    #     ''')

    #     self.conn.commit()

    # def create_main_interface(self):
    #     """Create the main interface with navigation"""
    #     # Header
    #     header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
    #     header_frame.pack(fill='x', padx=0, pady=0)
    #     header_frame.pack_propagate(False)

    #     title_label = tk.Label(header_frame, text="Inventory Management System",
    #                            font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
    #     title_label.pack(pady=20)

    #     # Navigation buttons
    #     nav_frame = tk.Frame(self.root, bg='#34495e', height=60)
    #     nav_frame.pack(fill='x')
    #     nav_frame.pack_propagate(False)

    #     button_style = {'font': ('Arial', 12), 'bg': '#3498db', 'fg': 'white',
    #                     'relief': 'flat', 'padx': 20, 'pady': 8}

    #     tk.Button(nav_frame, text="Categories", command=self.show_categories,
    #               **button_style).pack(side='left', padx=10, pady=10)
    #     tk.Button(nav_frame, text="Items", command=self.show_items,
    #               **button_style).pack(side='left', padx=10, pady=10)
    #     tk.Button(nav_frame, text="Customers", command=self.show_customers,
    #               **button_style).pack(side='left', padx=10, pady=10)
    #     tk.Button(nav_frame, text="Purchase", command=self.show_purchase,
    #               **button_style).pack(side='left', padx=10, pady=10)

    #     # Main content area
    #     self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
    #     self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    #     # Show categories by default
    #     self.show_categories()

    # def clear_main_frame(self):
    #     """Clear the main frame"""
    #     for widget in self.main_frame.winfo_children():
    #         widget.destroy()

    # def show_categories(self):
    #     """Show categories management interface"""
    #     self.clear_main_frame()

    #     # Title
    #     tk.Label(self.main_frame, text="Category Management",
    #              font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

    #     # Form frame
    #     form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Category",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
    #     form_frame.pack(fill='x', pady=10)

    #     # Form fields
    #     tk.Label(form_frame, text="Name:", bg='#f0f0f0').grid(
    #         row=0, column=0, sticky='w', pady=5)
    #     self.cat_name_entry = tk.Entry(form_frame, width=30)
    #     self.cat_name_entry.grid(row=0, column=1, pady=5, padx=10)

    #     tk.Label(form_frame, text="Description:", bg='#f0f0f0').grid(
    #         row=1, column=0, sticky='w', pady=5)
    #     self.cat_desc_entry = tk.Entry(form_frame, width=30)
    #     self.cat_desc_entry.grid(row=1, column=1, pady=5, padx=10)

    #     # Buttons
    #     button_frame = tk.Frame(form_frame, bg='#f0f0f0')
    #     button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    #     tk.Button(button_frame, text="Add Category", command=self.add_category,
    #               bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Update Category", command=self.update_category,
    #               bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Clear", command=self.clear_category_form,
    #               bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)

    #     # List frame
    #     list_frame = tk.LabelFrame(self.main_frame, text="Categories List",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
    #     list_frame.pack(fill='both', expand=True, pady=10)

    #     # Treeview for categories
    #     columns = ('ID', 'Name', 'Description', 'Created At')
    #     self.cat_tree = ttk.Treeview(
    #         list_frame, columns=columns, show='headings', height=10)

    #     for col in columns:
    #         self.cat_tree.heading(col, text=col)
    #         self.cat_tree.column(col, width=200)

    #     scrollbar = ttk.Scrollbar(
    #         list_frame, orient='vertical', command=self.cat_tree.yview)
    #     self.cat_tree.configure(yscrollcommand=scrollbar.set)

    #     self.cat_tree.pack(side='left', fill='both', expand=True)
    #     scrollbar.pack(side='right', fill='y')

    #     # Bind double-click event
    #     self.cat_tree.bind('<Double-1>', self.load_category_data)

    #     # Context menu
    #     self.cat_menu = tk.Menu(self.root, tearoff=0)
    #     self.cat_menu.add_command(
    #         label="Edit", command=self.load_category_data)
    #     self.cat_menu.add_command(label="Delete", command=self.delete_category)
    #     self.cat_tree.bind('<Button-3>', self.show_cat_context_menu)

    #     self.load_categories()

    # def add_category(self):
    #     """Add new category"""
    #     name = self.cat_name_entry.get().strip()
    #     description = self.cat_desc_entry.get().strip()

    #     if not name:
    #         messagebox.showerror("Error", "Category name is required!")
    #         return

    #     try:
    #         category_id = str(uuid.uuid4())
    #         self.cursor.execute('''
    #             INSERT INTO categories (id, name, description)
    #             VALUES (?, ?, ?)
    #         ''', (category_id, name, description))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Category added successfully!")
    #         self.clear_category_form()
    #         self.load_categories()
    #     except sqlite3.IntegrityError:
    #         messagebox.showerror("Error", "Category name already exists!")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error adding category: {str(e)}")

    # def update_category(self):
    #     """Update selected category"""
    #     selected = self.cat_tree.selection()
    #     if not selected:
    #         messagebox.showerror(
    #             "Error", "Please select a category to update!")
    #         return

    #     name = self.cat_name_entry.get().strip()
    #     description = self.cat_desc_entry.get().strip()

    #     if not name:
    #         messagebox.showerror("Error", "Category name is required!")
    #         return

    #     try:
    #         item = self.cat_tree.item(selected[0])
    #         category_id = item['values'][0]

    #         self.cursor.execute('''
    #             UPDATE categories SET name = ?, description = ?
    #             WHERE id = ?
    #         ''', (name, description, category_id))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Category updated successfully!")
    #         self.clear_category_form()
    #         self.load_categories()
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error updating category: {str(e)}")

    # def delete_category(self):
    #     """Delete selected category"""
    #     selected = self.cat_tree.selection()
    #     if not selected:
    #         messagebox.showerror(
    #             "Error", "Please select a category to delete!")
    #         return

    #     if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
    #         try:
    #             item = self.cat_tree.item(selected[0])
    #             category_id = item['values'][0]

    #             self.cursor.execute(
    #                 'DELETE FROM categories WHERE id = ?', (category_id,))
    #             self.conn.commit()
    #             messagebox.showinfo(
    #                 "Success", "Category deleted successfully!")
    #             self.load_categories()
    #         except Exception as e:
    #             messagebox.showerror(
    #                 "Error", f"Error deleting category: {str(e)}")

    # def load_category_data(self, event=None):
    #     """Load category data into form"""
    #     selected = self.cat_tree.selection()
    #     if selected:
    #         item = self.cat_tree.item(selected[0])
    #         values = item['values']

    #         self.cat_name_entry.delete(0, tk.END)
    #         self.cat_name_entry.insert(0, values[1])

    #         self.cat_desc_entry.delete(0, tk.END)
    #         self.cat_desc_entry.insert(0, values[2])

    # def clear_category_form(self):
    #     """Clear category form"""
    #     self.cat_name_entry.delete(0, tk.END)
    #     self.cat_desc_entry.delete(0, tk.END)

    # def load_categories(self):
    #     """Load categories into treeview"""
    #     for item in self.cat_tree.get_children():
    #         self.cat_tree.delete(item)

    #     self.cursor.execute(
    #         'SELECT id, name, description, created_at FROM categories ORDER BY name')
    #     for row in self.cursor.fetchall():
    #         self.cat_tree.insert('', 'end', values=row)

    # def show_cat_context_menu(self, event):
    #     """Show context menu for categories"""
    #     self.cat_menu.post(event.x_root, event.y_root)

    # def show_items(self):
    #     """Show items management interface"""
    #     self.clear_main_frame()

    #     # Title
    #     tk.Label(self.main_frame, text="Items Management",
    #              font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

    #     # Form frame
    #     form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Item",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
    #     form_frame.pack(fill='x', pady=10)

    #     # First row
    #     row1 = tk.Frame(form_frame, bg='#f0f0f0')
    #     row1.pack(fill='x', pady=5)

    #     tk.Label(row1, text="Name:", bg='#f0f0f0').pack(side='left')
    #     self.item_name_entry = tk.Entry(row1, width=20)
    #     self.item_name_entry.pack(side='left', padx=10)

    #     tk.Label(row1, text="Serial No:", bg='#f0f0f0').pack(
    #         side='left', padx=(20, 0))
    #     self.item_serial_entry = tk.Entry(row1, width=20)
    #     self.item_serial_entry.pack(side='left', padx=10)

    #     # Second row
    #     row2 = tk.Frame(form_frame, bg='#f0f0f0')
    #     row2.pack(fill='x', pady=5)

    #     tk.Label(row2, text="Category:", bg='#f0f0f0').pack(side='left')
    #     self.item_category_combo = ttk.Combobox(row2, width=18)
    #     self.item_category_combo.pack(side='left', padx=10)

    #     tk.Label(row2, text="Price:", bg='#f0f0f0').pack(
    #         side='left', padx=(20, 0))
    #     self.item_price_entry = tk.Entry(row2, width=20)
    #     self.item_price_entry.pack(side='left', padx=10)

    #     # Third row
    #     row3 = tk.Frame(form_frame, bg='#f0f0f0')
    #     row3.pack(fill='x', pady=5)

    #     tk.Label(row3, text="Total Quantity:", bg='#f0f0f0').pack(side='left')
    #     self.item_total_entry = tk.Entry(row3, width=20)
    #     self.item_total_entry.pack(side='left', padx=10)

    #     tk.Label(row3, text="Available:", bg='#f0f0f0').pack(
    #         side='left', padx=(20, 0))
    #     self.item_available_entry = tk.Entry(row3, width=20)
    #     self.item_available_entry.pack(side='left', padx=10)

    #     # Buttons
    #     button_frame = tk.Frame(form_frame, bg='#f0f0f0')
    #     button_frame.pack(pady=10)

    #     tk.Button(button_frame, text="Add Item", command=self.add_item,
    #               bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Update Item", command=self.update_item,
    #               bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Clear", command=self.clear_item_form,
    #               bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)

    #     # List frame
    #     list_frame = tk.LabelFrame(self.main_frame, text="Items List",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
    #     list_frame.pack(fill='both', expand=True, pady=10)

    #     # Treeview for items
    #     columns = ('ID', 'Name', 'Serial No', 'Category',
    #                'Total', 'Available', 'Price')
    #     self.item_tree = ttk.Treeview(
    #         list_frame, columns=columns, show='headings', height=10)

    #     for col in columns:
    #         self.item_tree.heading(col, text=col)
    #         if col == 'ID':
    #             self.item_tree.column(col, width=0, stretch=False)
    #         else:
    #             self.item_tree.column(col, width=120)

    #     scrollbar2 = ttk.Scrollbar(
    #         list_frame, orient='vertical', command=self.item_tree.yview)
    #     self.item_tree.configure(yscrollcommand=scrollbar2.set)

    #     self.item_tree.pack(side='left', fill='both', expand=True)
    #     scrollbar2.pack(side='right', fill='y')

    #     # Bind events
    #     self.item_tree.bind('<Double-1>', self.load_item_data)

    #     # Context menu
    #     self.item_menu = tk.Menu(self.root, tearoff=0)
    #     self.item_menu.add_command(label="Edit", command=self.load_item_data)
    #     self.item_menu.add_command(label="Delete", command=self.delete_item)
    #     self.item_tree.bind('<Button-3>', self.show_item_context_menu)

    #     self.load_item_categories()
    #     self.load_items()

    # def load_item_categories(self):
    #     """Load categories for item form"""
    #     self.cursor.execute('SELECT id, name FROM categories ORDER BY name')
    #     categories = self.cursor.fetchall()
    #     self.item_category_combo['values'] = [
    #         f"{cat[1]} ({cat[0][:8]})" for cat in categories]

    # def add_item(self):
    #     """Add new item"""
    #     name = self.item_name_entry.get().strip()
    #     serial_no = self.item_serial_entry.get().strip()
    #     category = self.item_category_combo.get()

    #     try:
    #         total_amount = int(self.item_total_entry.get())
    #         available_amount = int(self.item_available_entry.get())
    #         price = float(self.item_price_entry.get())
    #     except ValueError:
    #         messagebox.showerror(
    #             "Error", "Please enter valid numbers for amounts and price!")
    #         return

    #     if not all([name, serial_no, category]):
    #         messagebox.showerror("Error", "All fields are required!")
    #         return

    #     # Extract category ID
    #     category_id = category.split('(')[1].rstrip(')')

    #     try:
    #         item_id = str(uuid.uuid4())
    #         self.cursor.execute('''
    #             INSERT INTO items (id, name, serial_no, category_id, total_amount, available_amount, price)
    #             VALUES (?, ?, ?, ?, ?, ?, ?)
    #         ''', (item_id, name, serial_no, category_id, total_amount, available_amount, price))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Item added successfully!")
    #         self.clear_item_form()
    #         self.load_items()
    #     except sqlite3.IntegrityError:
    #         messagebox.showerror("Error", "Serial number already exists!")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error adding item: {str(e)}")

    # def update_item(self):
    #     """Update selected item"""
    #     selected = self.item_tree.selection()
    #     if not selected:
    #         messagebox.showerror("Error", "Please select an item to update!")
    #         return

    #     name = self.item_name_entry.get().strip()
    #     serial_no = self.item_serial_entry.get().strip()
    #     category = self.item_category_combo.get()

    #     try:
    #         total_amount = int(self.item_total_entry.get())
    #         available_amount = int(self.item_available_entry.get())
    #         price = float(self.item_price_entry.get())
    #     except ValueError:
    #         messagebox.showerror(
    #             "Error", "Please enter valid numbers for amounts and price!")
    #         return

    #     if not all([name, serial_no, category]):
    #         messagebox.showerror("Error", "All fields are required!")
    #         return

    #     # Extract category ID
    #     category_id = category.split('(')[1].rstrip(')')

    #     try:
    #         item = self.item_tree.item(selected[0])
    #         item_id = item['values'][0]

    #         self.cursor.execute('''
    #             UPDATE items SET name = ?, serial_no = ?, category_id = ?,
    #             total_amount = ?, available_amount = ?, price = ?
    #             WHERE id = ?
    #         ''', (name, serial_no, category_id, total_amount, available_amount, price, item_id))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Item updated successfully!")
    #         self.clear_item_form()
    #         self.load_items()
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error updating item: {str(e)}")

    # def delete_item(self):
    #     """Delete selected item"""
    #     selected = self.item_tree.selection()
    #     if not selected:
    #         messagebox.showerror("Error", "Please select an item to delete!")
    #         return

    #     if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
    #         try:
    #             item = self.item_tree.item(selected[0])
    #             item_id = item['values'][0]

    #             self.cursor.execute(
    #                 'DELETE FROM items WHERE id = ?', (item_id,))
    #             self.conn.commit()
    #             messagebox.showinfo("Success", "Item deleted successfully!")
    #             self.load_items()
    #         except Exception as e:
    #             messagebox.showerror("Error", f"Error deleting item: {str(e)}")

    # def load_item_data(self, event=None):
    #     """Load item data into form"""
    #     selected = self.item_tree.selection()
    #     if selected:
    #         item = self.item_tree.item(selected[0])
    #         values = item['values']

    #         self.item_name_entry.delete(0, tk.END)
    #         self.item_name_entry.insert(0, values[1])

    #         self.item_serial_entry.delete(0, tk.END)
    #         self.item_serial_entry.insert(0, values[2])

    #         # Find and set category
    #         for cat in self.item_category_combo['values']:
    #             if values[3] in cat:
    #                 self.item_category_combo.set(cat)
    #                 break

    #         self.item_total_entry.delete(0, tk.END)
    #         self.item_total_entry.insert(0, values[4])

    #         self.item_available_entry.delete(0, tk.END)
    #         self.item_available_entry.insert(0, values[5])

    #         self.item_price_entry.delete(0, tk.END)
    #         self.item_price_entry.insert(0, values[6])

    # def clear_item_form(self):
    #     """Clear item form"""
    #     self.item_name_entry.delete(0, tk.END)
    #     self.item_serial_entry.delete(0, tk.END)
    #     self.item_category_combo.set('')
    #     self.item_total_entry.delete(0, tk.END)
    #     self.item_available_entry.delete(0, tk.END)
    #     self.item_price_entry.delete(0, tk.END)

    # def load_items(self):
    #     """Load items into treeview"""
    #     for item in self.item_tree.get_children():
    #         self.item_tree.delete(item)

    #     self.cursor.execute('''
    #         SELECT i.id, i.name, i.serial_no, c.name, i.total_amount, i.available_amount, i.price
    #         FROM items i
    #         LEFT JOIN categories c ON i.category_id = c.id
    #         ORDER BY i.name
    #     ''')
    #     for row in self.cursor.fetchall():
    #         self.item_tree.insert('', 'end', values=row)

    # def show_item_context_menu(self, event):
    #     """Show context menu for items"""
    #     self.item_menu.post(event.x_root, event.y_root)

    # def show_customers(self):
    #     """Show customers management interface"""
    #     self.clear_main_frame()

    #     # Title
    #     tk.Label(self.main_frame, text="Customer Management",
    #              font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

    #     # Form frame
    #     form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Customer",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
    #     form_frame.pack(fill='x', pady=10)

    #     # Form fields
    #     tk.Label(form_frame, text="Name:", bg='#f0f0f0').grid(
    #         row=0, column=0, sticky='w', pady=5)
    #     self.cust_name_entry = tk.Entry(form_frame, width=30)
    #     self.cust_name_entry.grid(row=0, column=1, pady=5, padx=10)

    #     tk.Label(form_frame, text="Mobile:", bg='#f0f0f0').grid(
    #         row=1, column=0, sticky='w', pady=5)
    #     self.cust_mobile_entry = tk.Entry(form_frame, width=30)
    #     self.cust_mobile_entry.grid(row=1, column=1, pady=5, padx=10)

    #     # Buttons
    #     button_frame = tk.Frame(form_frame, bg='#f0f0f0')
    #     button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    #     tk.Button(button_frame, text="Add Customer", command=self.add_customer,
    #               bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Update Customer", command=self.update_customer,
    #               bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
    #     tk.Button(button_frame, text="Clear", command=self.clear_customer_form,
    #               bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)

    #     # List frame
    #     list_frame = tk.LabelFrame(self.main_frame, text="Customers List",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
    #     list_frame.pack(fill='both', expand=True, pady=10)

    #     # Treeview for customers
    #     columns = ('ID', 'Name', 'Mobile', 'Created At')
    #     self.cust_tree = ttk.Treeview(
    #         list_frame, columns=columns, show='headings', height=10)

    #     for col in columns:
    #         self.cust_tree.heading(col, text=col)
    #         self.cust_tree.column(col, width=200)

    #     scrollbar3 = ttk.Scrollbar(
    #         list_frame, orient='vertical', command=self.cust_tree.yview)
    #     self.cust_tree.configure(yscrollcommand=scrollbar3.set)

    #     self.cust_tree.pack(side='left', fill='both', expand=True)
    #     scrollbar3.pack(side='right', fill='y')

    #     # Bind events
    #     self.cust_tree.bind('<Double-1>', self.load_customer_data)

    #     # Context menu
    #     self.cust_menu = tk.Menu(self.root, tearoff=0)
    #     self.cust_menu.add_command(
    #         label="Edit", command=self.load_customer_data)
    #     self.cust_menu.add_command(
    #         label="Delete", command=self.delete_customer)
    #     self.cust_tree.bind('<Button-3>', self.show_cust_context_menu)

    #     self.load_customers()

    # def add_customer(self):
    #     """Add new customer"""
    #     name = self.cust_name_entry.get().strip()
    #     mobile = self.cust_mobile_entry.get().strip()

    #     if not all([name, mobile]):
    #         messagebox.showerror("Error", "All fields are required!")
    #         return

    #     try:
    #         customer_id = str(uuid.uuid4())
    #         self.cursor.execute('''
    #             INSERT INTO customers (id, name, mobile)
    #             VALUES (?, ?, ?)
    #         ''', (customer_id, name, mobile))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Customer added successfully!")
    #         self.clear_customer_form()
    #         self.load_customers()
    #     except sqlite3.IntegrityError:
    #         messagebox.showerror("Error", "Mobile number already exists!")
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error adding customer: {str(e)}")

    # def update_customer(self):
    #     """Update selected customer"""
    #     selected = self.cust_tree.selection()
    #     if not selected:
    #         messagebox.showerror(
    #             "Error", "Please select a customer to update!")
    #         return

    #     name = self.cust_name_entry.get().strip()
    #     mobile = self.cust_mobile_entry.get().strip()

    #     if not all([name, mobile]):
    #         messagebox.showerror("Error", "All fields are required!")
    #         return

    #     try:
    #         item = self.cust_tree.item(selected[0])
    #         customer_id = item['values'][0]

    #         self.cursor.execute('''
    #             UPDATE customers SET name = ?, mobile = ?
    #             WHERE id = ?
    #         ''', (name, mobile, customer_id))
    #         self.conn.commit()
    #         messagebox.showinfo("Success", "Customer updated successfully!")
    #         self.clear_customer_form()
    #         self.load_customers()
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Error updating customer: {str(e)}")

    # def delete_customer(self):
    #     """Delete selected customer"""
    #     selected = self.cust_tree.selection()
    #     if not selected:
    #         messagebox.showerror(
    #             "Error", "Please select a customer to delete!")
    #         return

    #     if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
    #         try:
    #             item = self.cust_tree.item(selected[0])
    #             customer_id = item['values'][0]

    #             self.cursor.execute(
    #                 'DELETE FROM customers WHERE id = ?', (customer_id,))
    #             self.conn.commit()
    #             messagebox.showinfo(
    #                 "Success", "Customer deleted successfully!")
    #             self.load_customers()
    #         except Exception as e:
    #             messagebox.showerror(
    #                 "Error", f"Error deleting customer: {str(e)}")

    # def load_customer_data(self, event=None):
    #     """Load customer data into form"""
    #     selected = self.cust_tree.selection()
    #     if selected:
    #         item = self.cust_tree.item(selected[0])
    #         values = item['values']

    #         self.cust_name_entry.delete(0, tk.END)
    #         self.cust_name_entry.insert(0, values[1])

    #         self.cust_mobile_entry.delete(0, tk.END)
    #         self.cust_mobile_entry.insert(0, values[2])

    # def clear_customer_form(self):
    #     """Clear customer form"""
    #     self.cust_name_entry.delete(0, tk.END)
    #     self.cust_mobile_entry.delete(0, tk.END)

    # def load_customers(self):
    #     """Load customers into treeview"""
    #     for item in self.cust_tree.get_children():
    #         self.cust_tree.delete(item)

    #     self.cursor.execute(
    #         'SELECT id, name, mobile, created_at FROM customers ORDER BY name')
    #     for row in self.cursor.fetchall():
    #         self.cust_tree.insert('', 'end', values=row)

    # def show_cust_context_menu(self, event):
    #     """Show context menu for customers"""
    #     self.cust_menu.post(event.x_root, event.y_root)

    # def show_purchase(self):
    #     """Show purchase interface"""
    #     self.clear_main_frame()

    #     # Title
    #     tk.Label(self.main_frame, text="Purchase Management",
    #              font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

    #     # Customer info frame
    #     cust_frame = tk.LabelFrame(self.main_frame, text="Customer Information",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
    #     cust_frame.pack(fill='x', pady=10)

    #     row1 = tk.Frame(cust_frame, bg='#f0f0f0')
    #     row1.pack(fill='x', pady=5)

    #     tk.Label(row1, text="Mobile:", bg='#f0f0f0').pack(side='left')
    #     self.purchase_mobile_entry = tk.Entry(row1, width=20)
    #     self.purchase_mobile_entry.pack(side='left', padx=10)
    #     self.purchase_mobile_entry.bind('<KeyRelease>', self.search_customer)

    #     tk.Label(row1, text="Name:", bg='#f0f0f0').pack(
    #         side='left', padx=(20, 0))
    #     self.purchase_name_entry = tk.Entry(row1, width=30)
    #     self.purchase_name_entry.pack(side='left', padx=10)

    #     # Item entry frame
    #     item_frame = tk.LabelFrame(self.main_frame, text="Add Items",
    #                                font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
    #     item_frame.pack(fill='x', pady=10)

    #     row2 = tk.Frame(item_frame, bg='#f0f0f0')
    #     row2.pack(fill='x', pady=5)

    #     tk.Label(row2, text="Serial No:", bg='#f0f0f0').pack(side='left')
    #     self.purchase_serial_entry = tk.Entry(row2, width=20)
    #     self.purchase_serial_entry.pack(side='left', padx=10)

    #     tk.Label(row2, text="Quantity:", bg='#f0f0f0').pack(
    #         side='left', padx=(20, 0))
    #     self.purchase_qty_entry = tk.Entry(row2, width=10)
    #     self.purchase_qty_entry.pack(side='left', padx=10)

    #     tk.Button(row2, text="Add Item", command=self.add_purchase_item,
    #               bg='#3498db', fg='white', padx=20).pack(side='left', padx=20)

    #     # Purchase items table
    #     table_frame = tk.LabelFrame(self.main_frame, text="Purchase Items",
    #                                 font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
    #     table_frame.pack(fill='both', expand=True, pady=10)

    #     # Treeview for purchase items
    #     columns = ('Serial No', 'Item Name', 'Quantity',
    #                'Unit Price', 'Total Price')
    #     self.purchase_tree = ttk.Treeview(
    #         table_frame, columns=columns, show='headings', height=8)

    #     for col in columns:
    #         self.purchase_tree.heading(col, text=col)
    #         self.purchase_tree.column(col, width=150)

    #     scrollbar4 = ttk.Scrollbar(
    #         table_frame, orient='vertical', command=self.purchase_tree.yview)
    #     self.purchase_tree.configure(yscrollcommand=scrollbar4.set)

    #     self.purchase_tree.pack(side='left', fill='both', expand=True)
    #     scrollbar4.pack(side='right', fill='y')

    #     # Bottom frame for total and actions
    #     bottom_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
    #     bottom_frame.pack(fill='x', pady=10)

    #     # Total amount
    #     total_frame = tk.Frame(bottom_frame, bg='#f0f0f0')
    #     total_frame.pack(side='right')

    #     tk.Label(total_frame, text="Total Amount: ₹", font=(
    #         'Arial', 14, 'bold'), bg='#f0f0f0').pack(side='left')
    #     self.total_label = tk.Label(total_frame, text="0.00", font=('Arial', 14, 'bold'),
    #                                 fg='#e74c3c', bg='#f0f0f0')
    #     self.total_label.pack(side='left')

    #     # Actions frame
    #     action_frame = tk.Frame(bottom_frame, bg='#f0f0f0')
    #     action_frame.pack(side='left')

    #     self.generate_receipt_var = tk.BooleanVar()
    #     tk.Checkbutton(action_frame, text="Generate Receipt (PDF)", variable=self.generate_receipt_var,
    #                    bg='#f0f0f0', font=('Arial', 10)).pack(side='left', padx=10)

    #     tk.Button(action_frame, text="Complete Purchase", command=self.complete_purchase,
    #               bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side='left', padx=10)

    #     tk.Button(action_frame, text="Clear All", command=self.clear_purchase,
    #               bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)

    #     # Initialize purchase items list
    #     self.purchase_items = []

    #     # Context menu for purchase items
    #     self.purchase_menu = tk.Menu(self.root, tearoff=0)
    #     self.purchase_menu.add_command(
    #         label="Remove Item", command=self.remove_purchase_item)
    #     self.purchase_tree.bind('<Button-3>', self.show_purchase_context_menu)

    # def search_customer(self, event=None):
    #     """Search customer by mobile number"""
    #     mobile = self.purchase_mobile_entry.get().strip()
    #     if len(mobile) >= 10:  # Search when mobile has at least 10 digits
    #         self.cursor.execute(
    #             'SELECT name FROM customers WHERE mobile = ?', (mobile,))
    #         result = self.cursor.fetchone()

    #         if result:
    #             self.purchase_name_entry.delete(0, tk.END)
    #             self.purchase_name_entry.insert(0, result[0])
    #         else:
    #             self.purchase_name_entry.delete(0, tk.END)

    # def add_purchase_item(self):
    #     """Add item to purchase"""
    #     serial_no = self.purchase_serial_entry.get().strip()
    #     try:
    #         quantity = int(self.purchase_qty_entry.get())
    #     except ValueError:
    #         messagebox.showerror("Error", "Please enter a valid quantity!")
    #         return

    #     if not serial_no or quantity <= 0:
    #         messagebox.showerror(
    #             "Error", "Please enter serial number and valid quantity!")
    #         return

    #     # Check if item exists
    #     self.cursor.execute('''
    #         SELECT id, name, available_amount, price FROM items
    #         WHERE serial_no = ?
    #     ''', (serial_no,))
    #     item = self.cursor.fetchone()

    #     if not item:
    #         messagebox.showerror(
    #             "Error", "Item with this serial number not found!")
    #         return

    #     item_id, item_name, available_amount, price = item

    #     if quantity > available_amount:
    #         messagebox.showerror(
    #             "Error", f"Only {available_amount} items available!")
    #         return

    #     # Check if item already in purchase list
    #     for purchase_item in self.purchase_items:
    #         if purchase_item['serial_no'] == serial_no:
    #             messagebox.showerror(
    #                 "Error", "Item already added to purchase!")
    #             return

    #     # Add to purchase items
    #     total_price = quantity * price
    #     purchase_item = {
    #         'item_id': item_id,
    #         'serial_no': serial_no,
    #         'name': item_name,
    #         'quantity': quantity,
    #         'unit_price': price,
    #         'total_price': total_price
    #     }

    #     self.purchase_items.append(purchase_item)

    #     # Add to treeview
    #     self.purchase_tree.insert('', 'end', values=(
    #         serial_no, item_name, quantity, f"₹{price:.2f}", f"₹{total_price:.2f}"
    #     ))

    #     # Update total
    #     self.update_purchase_total()

    #     # Clear entries
    #     self.purchase_serial_entry.delete(0, tk.END)
    #     self.purchase_qty_entry.delete(0, tk.END)

    # def remove_purchase_item(self):
    #     """Remove selected item from purchase"""
    #     selected = self.purchase_tree.selection()
    #     if not selected:
    #         messagebox.showerror("Error", "Please select an item to remove!")
    #         return

    #     item = self.purchase_tree.item(selected[0])
    #     serial_no = item['values'][0]

    #     # Remove from purchase items list
    #     self.purchase_items = [
    #         item for item in self.purchase_items if item['serial_no'] != serial_no]

    #     # Remove from treeview
    #     self.purchase_tree.delete(selected[0])

    #     # Update total
    #     self.update_purchase_total()

    # def update_purchase_total(self):
    #     """Update total purchase amount"""
    #     total = sum(item['total_price'] for item in self.purchase_items)
    #     self.total_label.config(text=f"{total:.2f}")

    # def complete_purchase(self):
    #     """Complete the purchase"""
    #     mobile = self.purchase_mobile_entry.get().strip()
    #     name = self.purchase_name_entry.get().strip()

    #     if not mobile or not name:
    #         messagebox.showerror(
    #             "Error", "Customer mobile and name are required!")
    #         return

    #     if not self.purchase_items:
    #         messagebox.showerror(
    #             "Error", "Please add at least one item to purchase!")
    #         return

    #     try:
    #         # Check if customer exists
    #         self.cursor.execute(
    #             'SELECT id FROM customers WHERE mobile = ?', (mobile,))
    #         customer = self.cursor.fetchone()

    #         if not customer:
    #             # Create new customer
    #             customer_id = str(uuid.uuid4())
    #             self.cursor.execute('''
    #                 INSERT INTO customers (id, name, mobile)
    #                 VALUES (?, ?, ?)
    #             ''', (customer_id, name, mobile))
    #         else:
    #             customer_id = customer[0]

    #         # Create purchase record
    #         purchase_id = str(uuid.uuid4())
    #         total_amount = sum(item['total_price']
    #                            for item in self.purchase_items)

    #         self.cursor.execute('''
    #             INSERT INTO purchases (id, customer_id, total_amount)
    #             VALUES (?, ?, ?)
    #         ''', (purchase_id, customer_id, total_amount))

    #         # Add purchase items and update inventory
    #         for item in self.purchase_items:
    #             # Add to purchase_items table
    #             purchase_item_id = str(uuid.uuid4())
    #             self.cursor.execute('''
    #                 INSERT INTO purchase_items (id, purchase_id, item_id, quantity, unit_price, total_price)
    #                 VALUES (?, ?, ?, ?, ?, ?)
    #             ''', (purchase_item_id, purchase_id, item['item_id'], item['quantity'],
    #                   item['unit_price'], item['total_price']))

    #             # Update item available amount
    #             self.cursor.execute('''
    #                 UPDATE items SET available_amount = available_amount - ?
    #                 WHERE id = ?
    #             ''', (item['quantity'], item['item_id']))

    #         self.conn.commit()

    #         # Generate receipt if requested
    #         if self.generate_receipt_var.get():
    #             self.generate_receipt(purchase_id, customer_id, name, mobile)

    #         messagebox.showinfo("Success", "Purchase completed successfully!")
    #         self.clear_purchase()

    #     except Exception as e:
    #         self.conn.rollback()
    #         messagebox.showerror(
    #             "Error", f"Error completing purchase: {str(e)}")

    # def generate_receipt(self, purchase_id, customer_id, customer_name, customer_mobile):
    #     """Generate PDF receipt"""
    #     try:
    #         # Get purchase details
    #         self.cursor.execute('''
    #             SELECT p.purchase_date, p.total_amount,
    #                    pi.quantity, pi.unit_price, pi.total_price,
    #                    i.name, i.serial_no
    #             FROM purchases p
    #             JOIN purchase_items pi ON p.id = pi.purchase_id
    #             JOIN items i ON pi.item_id = i.id
    #             WHERE p.id = ?
    #         ''', (purchase_id,))

    #         purchase_data = self.cursor.fetchall()

    #         if not purchase_data:
    #             messagebox.showerror("Error", "No purchase data found!")
    #             return

    #         # Create PDF
    #         filename = f"receipt_{purchase_id[:8]}.pdf"
    #         filepath = filedialog.asksaveasfilename(
    #             defaultextension=".pdf",
    #             filetypes=[("PDF files", "*.pdf")],
    #             initialname=filename
    #         )

    #         if not filepath:
    #             return

    #         doc = SimpleDocTemplate(filepath, pagesize=letter)
    #         elements = []
    #         styles = getSampleStyleSheet()

    #         # Title
    #         title = Paragraph("PURCHASE RECEIPT", styles['Title'])
    #         elements.append(title)
    #         elements.append(Spacer(1, 20))

    #         # Customer info
    #         customer_info = [
    #             ['Customer Name:', customer_name],
    #             ['Mobile Number:', customer_mobile],
    #             ['Purchase Date:', purchase_data[0][0]],
    #             ['Receipt ID:', purchase_id[:8]]
    #         ]

    #         customer_table = Table(customer_info, colWidths=[2*72, 4*72])
    #         customer_table.setStyle(TableStyle([
    #             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
    #             ('FONTSIZE', (0, 0), (-1, -1), 10),
    #             ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    #             ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    #             ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    #         ]))

    #         elements.append(customer_table)
    #         elements.append(Spacer(1, 20))

    #         # Items table
    #         items_data = [['Item Name', 'Serial No',
    #                        'Quantity', 'Unit Price', 'Total Price']]

    #         for row in purchase_data:
    #             items_data.append([
    #                 row[5],  # item name
    #                 row[6],  # serial no
    #                 str(row[2]),  # quantity
    #                 f"₹{row[3]:.2f}",  # unit price
    #                 f"₹{row[4]:.2f}"   # total price
    #             ])

    #         items_table = Table(items_data, colWidths=[
    #                             2*72, 1.5*72, 1*72, 1.25*72, 1.25*72])
    #         items_table.setStyle(TableStyle([
    #             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    #             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    #             ('FONTSIZE', (0, 0), (-1, 0), 10),
    #             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    #             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    #             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    #             ('FONTSIZE', (0, 1), (-1, -1), 9),
    #             ('GRID', (0, 0), (-1, -1), 1, colors.black)
    #         ]))

    #         elements.append(items_table)
    #         elements.append(Spacer(1, 20))

    #         # Total
    #         total_data = [['TOTAL AMOUNT:', f"₹{purchase_data[0][1]:.2f}"]]
    #         total_table = Table(total_data, colWidths=[5*72, 2*72])
    #         total_table.setStyle(TableStyle([
    #             ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    #             ('FONTSIZE', (0, 0), (-1, -1), 14),
    #             ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
    #             ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    #             ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
    #             ('BOX', (0, 0), (-1, -1), 2, colors.black),
    #         ]))

    #         elements.append(total_table)

    #         # Build PDF
    #         doc.build(elements)
    #         messagebox.showinfo("Success", f"Receipt saved as {filepath}")

    #     except Exception as e:
    #         messagebox.showerror(
    #             "Error", f"Error generating receipt: {str(e)}")

    # def clear_purchase(self):
    #     """Clear purchase form"""
    #     self.purchase_mobile_entry.delete(0, tk.END)
    #     self.purchase_name_entry.delete(0, tk.END)
    #     self.purchase_serial_entry.delete(0, tk.END)
    #     self.purchase_qty_entry.delete(0, tk.END)

    #     # Clear purchase items
    #     for item in self.purchase_tree.get_children():
    #         self.purchase_tree.delete(item)

    #     self.purchase_items = []
    #     self.generate_receipt_var.set(False)
    #     self.update_purchase_total()

    # def show_purchase_context_menu(self, event):
    #     """Show context menu for purchase items"""
    #     self.purchase_menu.post(event.x_root, event.y_root)

    # def __del__(self):
    #     """Close database connection"""
    #     if hasattr(self, 'conn'):
    #         self.conn.close()


def main():
    root = tk.Tk()
    InventoryManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
