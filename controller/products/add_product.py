from tkinter import messagebox
import sqlite3
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.products import ProductManagement


def add_product(self: "ProductManagement"):
    """Add new product"""
    name = self.item_name_entry.get().strip()
    serial_no = self.item_serial_entry.get().strip()
    category = self.item_category_combo.get()

    try:
        total_amount = int(self.item_total_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter valid numbers for Total Quantity!")
        return

    try:
        available_amount = int(self.item_available_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter valid numbers for Available Quantity!")
        return

    try:
        price = float(self.item_price_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter valid numbers for Price!")
        return

    if not all([name, serial_no, category]):
        messagebox.showerror("Error", "All fields are required!")
        return

    if total_amount < available_amount:
        messagebox.showerror(
            "Error", "Total Quantity cannot be less than Available Quantity!")
        return

    # Extract category ID
    category_id = self.categories_data_dict.get(category)

    if not category_id:
        messagebox.showerror("Error", "Invalid category selected!")
        return

    try:
        item_id = str(uuid.uuid4())
        new_item = (item_id, name, serial_no, category_id,
                    total_amount, available_amount, price)
        self.cursor.execute('''
            INSERT INTO items (id, name, serial_no, category_id, total_amount, available_amount, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', new_item)
        self.conn.commit()
        messagebox.showinfo("Success", "product added successfully!")
        self.clear_product_form()

        self.products_data_list.append(new_item)
        self.item_tree.insert('', 'end', values=new_item)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Serial number already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding product: {str(e)}")
