from tkinter import messagebox
from typing import TYPE_CHECKING
from controller.purchases.update_purchase_total import update_purchase_total

if TYPE_CHECKING:
    from ui.purchases import PurchaseManagement


def remove_purchase_item(self: "PurchaseManagement"):
    """Remove selected item from purchase"""
    selected = self.purchase_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select an item to remove!")
        return

    item = self.purchase_tree.item(selected[0])
    serial_no = item['values'][0]

    # Remove from purchase items list
    self.purchase_items = [
        item for item in self.purchase_items if item['serial_no'] != serial_no]

    # Remove from treeview
    self.purchase_tree.delete(selected[0])

    # Update total
    update_purchase_total(self)
