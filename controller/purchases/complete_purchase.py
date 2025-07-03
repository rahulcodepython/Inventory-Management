from tkinter import messagebox
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from ui.purchases import PurchaseManagement


def complete_purchase(self: "PurchaseManagement"):
    """Complete the purchase"""
    mobile = self.purchase_mobile_entry.get().strip()
    name = self.purchase_name_entry.get().strip()

    if not mobile or not name:
        messagebox.showerror(
            "Error", "Customer mobile and name are required!")
        return

    if not self.purchase_items:
        messagebox.showerror(
            "Error", "Please add at least one item to purchase!")
        return

    try:
        # Check if customer exists
        self.cursor.execute(
            'SELECT id FROM customers WHERE mobile = ?', (mobile,))
        customer = self.cursor.fetchone()

        if not customer:
            # Create new customer
            customer_id = str(uuid.uuid4())
            self.cursor.execute('''
                INSERT INTO customers (id, name, mobile)
                VALUES (?, ?, ?)
            ''', (customer_id, name, mobile))
        else:
            customer_id = customer[0]

        # Create purchase record
        purchase_id = str(uuid.uuid4())
        total_amount = sum(item['total_price']
                           for item in self.purchase_items)

        self.cursor.execute('''
            INSERT INTO purchases (id, customer_id, total_amount)
            VALUES (?, ?, ?)
        ''', (purchase_id, customer_id, total_amount))

        # Add purchase items and update inventory
        for item in self.purchase_items:
            # Add to purchase_items table
            purchase_item_id = str(uuid.uuid4())
            self.cursor.execute('''
                INSERT INTO purchase_items (id, purchase_id, item_id, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (purchase_item_id, purchase_id, item['item_id'], item['quantity'],
                  item['unit_price'], item['total_price']))

            # Update item available amount
            self.cursor.execute('''
                UPDATE items SET available_amount = available_amount - ?
                WHERE id = ?
            ''', (item['quantity'], item['item_id']))

        self.conn.commit()

        # # Generate receipt if requested
        # if self.generate_receipt_var.get():
        #     self.generate_receipt(purchase_id, customer_id, name, mobile)

        messagebox.showinfo("Success", "Purchase completed successfully!")
        self.clear_purchase()

    except Exception as e:
        self.conn.rollback()
        messagebox.showerror(
            "Error", f"Error completing purchase: {str(e)}")
