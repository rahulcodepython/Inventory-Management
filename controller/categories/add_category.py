from tkinter import messagebox
import sqlite3
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.categories import CategoryManagement


def add_category(self: "CategoryManagement"):
    """Add new category"""
    name = self.cat_name_entry.get().strip()
    description = self.cat_desc_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Category name is required!")
        return

    try:
        category_id = str(uuid.uuid4())
        self.cursor.execute('''
            INSERT INTO categories (id, name, description)
            VALUES (?, ?, ?)
        ''', (category_id, name, description))
        self.conn.commit()
        messagebox.showinfo("Success", "Category added successfully!")
        self.clear_category_form()

        # Add to categories_data_list and treeview
        new_row = (category_id, name, description)
        self.categories_data_list.append(new_row)
        self.cat_tree.insert('', 'end', values=new_row[1:])
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Category name already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding category: {str(e)}")
