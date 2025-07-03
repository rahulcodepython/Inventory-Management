from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.products import ProductManagement


def update_product(self: "ProductManagement"):
    """Update selected product"""
    selected = self.item_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select an product to update!")
        return

    name = self.item_name_entry.get().strip()
    serial_no = self.item_serial_entry.get().strip()
    category = self.item_category_combo.get()

    try:
        total_amount = int(self.item_total_entry.get())
        available_amount = int(self.item_available_entry.get())
        price = float(self.item_price_entry.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Please enter valid numbers for amounts and price!")
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
        item = self.item_tree.item(selected[0])
        index = self.item_tree.index(selected[0])
        item_id = item['values'][0]

        self.cursor.execute('''
            UPDATE items SET name = ?, serial_no = ?, category_id = ?,
            total_amount = ?, available_amount = ?, price = ?
            WHERE id = ?
        ''', (name, serial_no, category_id, total_amount, available_amount, price, item_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
        self.clear_product_form()

        updated_row = (item_id, name, serial_no, category,
                       total_amount, available_amount, price)

        self.products_data_list[index] = updated_row
        self.item_tree.item(selected[0], values=updated_row)
        self.item_tree.selection_remove(selected[0])
    except Exception as e:
        messagebox.showerror("Error", f"Error updating product: {str(e)}")
