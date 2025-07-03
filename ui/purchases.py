import tkinter as tk
from tkinter import ttk
from src.clear_main_frame import clear_main_frame
from controller.purchases.search_customer import search_customer
from controller.purchases.add_purchase import add_purchase_item
from controller.purchases.remove_purchase import remove_purchase_item
from controller.purchases.complete_purchase import complete_purchase
from controller.purchases.update_purchase_total import update_purchase_total


class PurchaseManagement:
    def __init__(self, root, main_frame, cursor, conn):
        self.root = root
        self.main_frame = main_frame
        self.cursor = cursor
        self.conn = conn

        self.purchase_items = []
        self.generate_receipt_var = tk.BooleanVar()

        self.purchase_menu = tk.Menu(self.root, tearoff=0)
        self.purchase_menu.add_command(
            label="Remove Item", command=lambda: remove_purchase_item(self=self))

    def show_purchase_context_menu(self, event):
        """Show context menu for purchase items"""
        self.purchase_menu.post(event.x_root, event.y_root)

    def clear_purchase(self):
        """Clear purchase form"""
        self.purchase_mobile_entry.delete(0, tk.END)
        self.purchase_name_entry.delete(0, tk.END)
        self.purchase_serial_entry.delete(0, tk.END)
        self.purchase_qty_entry.delete(0, tk.END)

        # Clear purchase items
        for item in self.purchase_tree.get_children():
            self.purchase_tree.delete(item)

        self.purchase_items = []
        self.generate_receipt_var.set(False)
        update_purchase_total(self)

    def show_purchase(self):
        """Setup the purchase management interface"""
        clear_main_frame(self.main_frame)

        # Title
        tk.Label(self.main_frame, text="Purchase Management",
                 font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=0)

        # Customer info frame
        cust_frame = tk.LabelFrame(self.main_frame, text="Customer Information",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
        cust_frame.pack(fill='x', pady=10)

        row1 = tk.Frame(cust_frame, bg='#f0f0f0')
        row1.pack(fill='x', pady=5)

        tk.Label(row1, text="Mobile:", bg='#f0f0f0').grid(
            row=0, column=0, padx=10, pady=5, sticky='w')
        self.purchase_mobile_entry = tk.Entry(row1)
        self.purchase_mobile_entry.grid(row=0, column=1, padx=10, pady=5)
        self.purchase_mobile_entry.bind(
            '<FocusOut>', lambda event: search_customer(self=self, event=event))

        tk.Label(row1, text="Name:", bg='#f0f0f0').grid(
            row=0, column=2, padx=10, pady=5, sticky='w')
        self.purchase_name_entry = tk.Entry(row1)
        self.purchase_name_entry.grid(row=0, column=3, padx=10, pady=5)

        # Item entry frame
        item_frame = tk.LabelFrame(self.main_frame, text="Add Items",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
        item_frame.pack(fill='x', pady=10)

        row2 = tk.Frame(item_frame, bg='#f0f0f0')
        row2.pack(fill='x', pady=5)

        tk.Label(row2, text="Serial No:", bg='#f0f0f0').grid(
            row=0, column=0, padx=10, pady=5, sticky='w')
        self.purchase_serial_entry = tk.Entry(row2)
        self.purchase_serial_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(row2, text="Quantity:", bg='#f0f0f0').grid(
            row=0, column=2, padx=10, pady=5, sticky='w')
        self.purchase_qty_entry = tk.Entry(row2)
        self.purchase_qty_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Button(row2, text="Add Item", command=lambda: add_purchase_item(self=self),
                  bg='#3498db', fg='white', padx=20).grid(row=0, column=4, padx=10, pady=5)

        # Purchase items table
        table_frame = tk.LabelFrame(self.main_frame, text="Purchase Items",
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        table_frame.pack(fill='both', expand=True, pady=10)

        # Treeview for purchase items
        columns = ('Serial No', 'Item Name', 'Quantity',
                   'Unit Price', 'Total Price')
        self.purchase_tree = ttk.Treeview(
            table_frame, columns=columns, show='headings', height=8)

        for col in columns:
            self.purchase_tree.heading(col, text=col)
            self.purchase_tree.column(col, width=150)

        scrollbar4 = ttk.Scrollbar(
            table_frame, orient='vertical', command=self.purchase_tree.yview)
        self.purchase_tree.configure(yscrollcommand=scrollbar4.set)

        self.purchase_tree.pack(side='left', fill='both', expand=True)
        scrollbar4.pack(side='right', fill='y')

        self.purchase_tree.bind('<Button-3>', self.show_purchase_context_menu)

        # Bottom frame for total and actions
        bottom_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        bottom_frame.pack(fill='x', pady=10)

        # Total amount
        total_frame = tk.Frame(bottom_frame, bg='#f0f0f0')
        total_frame.pack(side='right')

        tk.Label(total_frame, text="Total Amount: ₹", font=(
            'Arial', 14, 'bold'), bg='#f0f0f0').pack(side='left')
        self.total_label = tk.Label(total_frame, text="0.00", font=('Arial', 14, 'bold'),
                                    fg='#e74c3c', bg='#f0f0f0')
        self.total_label.pack(side='left')

        # Actions frame
        action_frame = tk.Frame(bottom_frame, bg='#f0f0f0')
        action_frame.pack(side='left')

        tk.Checkbutton(action_frame, text="Generate Receipt (PDF)", variable=self.generate_receipt_var,
                       bg='#f0f0f0', font=('Arial', 10)).pack(side='left', padx=10)

        tk.Button(action_frame, text="Complete Purchase", command=lambda: complete_purchase(self=self),
                  bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), padx=30).pack(side='left', padx=10)

        tk.Button(action_frame, text="Clear All", command=self.clear_purchase,
                  bg='#e74c3c', fg='white', padx=20).pack(side='left', padx=5)
