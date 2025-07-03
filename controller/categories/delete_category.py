from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.categories import CategoryManagement


def delete_category(self: "CategoryManagement"):
    """Delete selected category"""
    selected = self.cat_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Please select a category to delete!")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
        try:
            index = self.cat_tree.index(selected[0])
            category_id = self.categories_data_list[index][0]

            self.cursor.execute(
                'DELETE FROM categories WHERE id = ?', (category_id,))
            self.conn.commit()
            messagebox.showinfo(
                "Success", "Category deleted successfully!")

            self.categories_data_list.pop(index)
            self.cat_tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error deleting category: {str(e)}")
