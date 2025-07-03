import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING
from controller.purchases.update_purchase_total import update_purchase_total

if TYPE_CHECKING:
    from ui.purchases import PurchaseManagement


def add_purchase_item(self: "PurchaseManagement"):
    """Add item to purchase"""
    serial_no = self.purchase_serial_entry.get().strip()
    try:
        quantity = int(self.purchase_qty_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid quantity!")
        return

    if not serial_no or quantity <= 0:
        messagebox.showerror(
            "Error", "Please enter serial number and valid quantity!")
        return

    # Check if item exists
    self.cursor.execute('''
        SELECT id, name, available_amount, price FROM items
        WHERE serial_no = ?
    ''', (serial_no,))
    item = self.cursor.fetchone()

    if not item:
        messagebox.showerror(
            "Error", "Item with this serial number not found!")
        return

    item_id, item_name, available_amount, price = item

    if quantity > available_amount:
        messagebox.showerror(
            "Error", f"Only {available_amount} items available!")
        return

    # Check if item already in purchase list
    for purchase_item in self.purchase_items:
        if purchase_item['serial_no'] == serial_no:
            messagebox.showerror(
                "Error", "Item already added to purchase!")
            return

    # Add to purchase items
    total_price = quantity * price
    purchase_item = {
        'item_id': item_id,
        'serial_no': serial_no,
        'name': item_name,
        'quantity': quantity,
        'unit_price': price,
        'total_price': total_price
    }

    self.purchase_items.append(purchase_item)

    # Add to treeview
    self.purchase_tree.insert('', 'end', values=(
        serial_no, item_name, quantity, f"₹{price:.2f}", f"₹{total_price:.2f}"
    ))

    # Update total
    update_purchase_total(self)

    # Clear entries
    self.purchase_serial_entry.delete(0, tk.END)
    self.purchase_qty_entry.delete(0, tk.END)
