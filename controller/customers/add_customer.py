from tkinter import messagebox
import uuid
import sqlite3
from typing import TYPE_CHECKING
from src.date_formatter import format_date

if TYPE_CHECKING:
    from ui.customers import CustomerManagement


def add_customer(self: "CustomerManagement"):
    """Add new customer"""
    name = self.cust_name_entry.get().strip()
    mobile = self.cust_mobile_entry.get().strip()

    if not all([name, mobile]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        customer_id = str(uuid.uuid4())
        self.cursor.execute('''
            INSERT INTO customers (id, name, mobile)
            VALUES (?, ?, ?)
        ''', (customer_id, name, mobile))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer added successfully!")
        self.clear_customer_form()

        new_data = (customer_id, name, mobile, format_date())
        self.customer_data_list.append(new_data)
        self.cust_tree.insert('', 'end', values=new_data)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Mobile number already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding customer: {str(e)}")
