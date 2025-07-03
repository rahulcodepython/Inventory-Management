import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.purchases import PurchaseManagement


def search_customer(self: "PurchaseManagement", event=None):
    """Search customer by mobile number"""
    mobile = self.purchase_mobile_entry.get().strip()

    self.cursor.execute(
        'SELECT name FROM customers WHERE mobile = ?', (mobile,))
    result = self.cursor.fetchone()

    print(
        f"Searching for customer with mobile: {mobile} and the result is: {result}")

    if result:
        self.purchase_name_entry.delete(0, tk.END)
        self.purchase_name_entry.insert(0, result[0])
    else:
        self.purchase_name_entry.delete(0, tk.END)
