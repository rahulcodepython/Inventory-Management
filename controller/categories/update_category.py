from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.categories import CategoryManagement


def update_category(self: "CategoryManagement"):
    """Update selected category"""
    selected = self.cat_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Please select a category to update!")
        return

    name = self.cat_name_entry.get().strip()
    description = self.cat_desc_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Category name is required!")
        return

    try:
        item = self.cat_tree.item(selected[0])
        index = self.cat_tree.index(selected[0])
        category_id = item['values'][0]

        self.cursor.execute('''
            UPDATE categories SET name = ?, description = ?
            WHERE id = ?
        ''', (name, description, category_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Category updated successfully!")
        self.clear_category_form()

        updated_row = (category_id, name, description)
        self.categories_data_list[index] = updated_row
        self.cat_tree.item(selected[0], values=updated_row[1:])
        self.cat_tree.selection_remove(selected[0])

        self.show_add_button()  # Reset to add button after update
    except Exception as e:
        messagebox.showerror("Error", f"Error updating category: {str(e)}")
