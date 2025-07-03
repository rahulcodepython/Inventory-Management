import tkinter as tk
from src.init_database import init_database
from src.create_main_interface import create_main_interface
from ui.categories import CategoryManagement
from ui.products import ProductManagement
from ui.customers import CustomerManagement
from ui.purchases import PurchaseManagement
from ui.purchase_history import PurchaseHistoryManagement


class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        # Initialize database
        self.conn, self.cursor = init_database()

        self.main_frame = tk.Frame(root, bg='#f0f0f0')

        self.category_management = CategoryManagement(
            self.root, self.main_frame, self.cursor, self.conn)
        self.product_management = ProductManagement(
            self.root, self.main_frame, self.cursor, self.conn)
        self.customer_management = CustomerManagement(
            self.root, self.main_frame, self.cursor, self.conn)
        self.purchase_management = PurchaseManagement(
            self.root, self.main_frame, self.cursor, self.conn)
        self.purchase_history_management = PurchaseHistoryManagement(
            self.root, self.main_frame, self.cursor, self.conn)

        # Create main interface
        create_main_interface(
            self.root,
            self.main_frame,
            self.category_management.show_categories,
            self.product_management.show_products,
            self.customer_management.show_customers,
            self.purchase_management.show_purchase,
            self.purchase_history_management.show_history
        )


def main():
    root = tk.Tk()
    InventoryManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
