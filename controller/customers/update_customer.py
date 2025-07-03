from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.customers import CustomerManagement


def update_customer(self: "CustomerManagement"):
    """Update selected customer"""
    selected = self.cust_tree.selection()
    if not selected:
        messagebox.showerror(
            "Error", "Please select a customer to update!")
        return

    name = self.cust_name_entry.get().strip()
    mobile = self.cust_mobile_entry.get().strip()

    if not all([name, mobile]):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        item = self.cust_tree.item(selected[0])
        index = self.cust_tree.index(selected[0])
        customer_id = item['values'][0]

        self.cursor.execute('''
            UPDATE customers SET name = ?, mobile = ?
            WHERE id = ?
        ''', (name, mobile, customer_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully!")
        self.clear_customer_form()

        self.customer_data_list[index] = (
            customer_id, name, mobile, item['values'][3])
        self.cust_tree.item(selected[0], values=(
            customer_id, name, mobile, item['values'][3]))
        self.cust_tree.selection_remove(selected[0])
    except Exception as e:
        messagebox.showerror("Error", f"Error updating customer: {str(e)}")
