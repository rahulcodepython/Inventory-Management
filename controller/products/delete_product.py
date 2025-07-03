from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.products import ProductManagement


def delete_product(self: "ProductManagement"):
    """Delete selected product"""
    selected = self.item_tree.selection()

    if not selected:
        messagebox.showerror("Error", "Please select an item to delete!")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this item?"):
        try:
            item = self.item_tree.item(selected[0])
            index = self.item_tree.index(selected[0])
            item_id = item['values'][0]

            self.cursor.execute(
                'DELETE FROM items WHERE id = ?', (item_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Item deleted successfully!")

            self.products_data_list.pop(index)
            self.item_tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting item: {str(e)}")
