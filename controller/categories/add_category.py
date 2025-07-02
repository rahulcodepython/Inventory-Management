from tkinter import messagebox
import sqlite3
import uuid
from controller.categories.clear_category_form import clear_category_form


def add_category(cat_name_entry, cat_desc_entry, cat_tree, categories_data_list, cursor, conn):
    """Add new category"""
    name = cat_name_entry.get().strip()
    description = cat_desc_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Category name is required!")
        return

    try:
        category_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO categories (id, name, description)
            VALUES (?, ?, ?)
        ''', (category_id, name, description))
        conn.commit()
        messagebox.showinfo("Success", "Category added successfully!")
        clear_category_form(cat_name_entry, cat_desc_entry)

        # Add to categories_data_list and treeview
        new_row = (category_id, name, description)
        categories_data_list.append(new_row)
        cat_tree.insert('', 'end', values=new_row)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Category name already exists!")
    except Exception as e:
        messagebox.showerror("Error", f"Error adding category: {str(e)}")
