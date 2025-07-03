from tkinter import messagebox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.customers import CustomerManagement


def delete_customer(self: "CustomerManagement"):
    """Delete selected customer"""
    selected = self.cust_tree.selection()
    if not selected:
        messagebox.showerror(
            "Error", "Please select a customer to delete!")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
        try:
            item = self.cust_tree.item(selected[0])
            index = self.cust_tree.index(selected[0])
            customer_id = item['values'][0]

            self.cursor.execute(
                'DELETE FROM customers WHERE id = ?', (customer_id,))
            self.conn.commit()
            messagebox.showinfo(
                "Success", "Customer deleted successfully!")

            self.customer_data_list.pop(index)
            self.cust_tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error deleting customer: {str(e)}")
