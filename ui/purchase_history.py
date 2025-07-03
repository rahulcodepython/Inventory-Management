import tkinter as tk
from tkinter import ttk
from src.clear_main_frame import clear_main_frame
from controller.purchase_history.load_purchase_history import load_purchase_history


class PurchaseHistoryManagement:
    def __init__(self, root, main_frame, cursor, conn):
        self.root = root
        self.main_frame = main_frame
        self.cursor = cursor
        self.conn = conn

        self.purchases = load_purchase_history(self)

    def show_history(self):
        # Main frame
        clear_main_frame(self.main_frame)

        # Title
        tk.Label(self.main_frame, text="Purchase Records",
                 font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

        # Tree frame
        tree_frame = tk.LabelFrame(self.main_frame, text="All Records",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        tree_frame.pack(fill='x', pady=10)

        # Define columns
        columns = ('Type', 'Name', 'Mobile', 'Date', 'Amount', 'Details')

        # Create treeview
        self.tree = ttk.Treeview(
            tree_frame, columns=columns, show='tree headings', height=15)

        # Configure column headings
        self.tree.heading('#0', text='ID / Item', anchor='w')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Mobile', text='Mobile')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Amount', text='Amount')
        self.tree.heading('Details', text='Details')

        # Configure column widths
        self.tree.column('#0', width=200, minwidth=150)
        self.tree.column('Type', width=80, minwidth=60)
        self.tree.column('Name', width=100, minwidth=80)
        self.tree.column('Mobile', width=100, minwidth=80)
        self.tree.column('Date', width=100, minwidth=80)
        self.tree.column('Amount', width=100, minwidth=80)
        self.tree.column('Details', width=200, minwidth=150)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(
            tree_frame, orient='vertical', command=self.tree.yview)

        self.tree.configure(yscrollcommand=v_scrollbar.set)

        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')

        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_item_double_click)

        # Statistics frame
        stats_frame = ttk.LabelFrame(
            self.main_frame, text="Statistics", padding="10")
        stats_frame.pack(fill='x', pady=(10, 0))

        self.stats_label = ttk.Label(stats_frame, text="", font=('Arial', 10))
        self.stats_label.pack()

        self.populate_tree()

    def populate_tree(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_purchases = len(self.purchases)
        total_amount = sum(data['total_amount']
                           for data in self.purchases.values())

        # Add each purchase as a parent node
        for purchase_id, data in self.purchases.items():
            # Truncate long IDs for display
            display_id = purchase_id[:8] + \
                "..." if len(purchase_id) > 8 else purchase_id

            # Insert parent node (purchase record)
            parent = self.tree.insert('', 'end',
                                      text=display_id,
                                      values=('Purchase', data['name'], data['mobile'],
                                              data['date'], f"₹{data['total_amount']:.2f}",
                                              f"{len(data['items'])} items"),
                                      tags=('purchase',))

            # Add items as child nodes
            for i, item in enumerate(data['items'], 1):
                # Parse item details
                item_parts = item.split(' @')
                item_name = item_parts[0] if item_parts else item
                item_price = item_parts[1] if len(item_parts) > 1 else ""

                self.tree.insert(parent, 'end',
                                 text=f"Item {i}",
                                 values=('Item', item_name, '',
                                         '', item_price, item),
                                 tags=('item',))

        # Configure tags for styling
        self.tree.tag_configure(
            'purchase', background='#E8F4FD', foreground='#2E8B57')
        self.tree.tag_configure(
            'item', background='#F5F5F5', foreground='#333333')

        # Expand all nodes by default
        for item in self.tree.get_children():
            self.tree.item(item, open=True)

        # Update statistics
        self.update_statistics(total_purchases, total_amount)

    def update_statistics(self, total_purchases, total_amount):
        stats_text = f"Total Purchases: {total_purchases} | Total Amount: ₹{total_amount:.2f}"
        self.stats_label.config(text=stats_text)

    def on_item_double_click(self, event):
        item = self.tree.selection()
        print(item)
