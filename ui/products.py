import tkinter as tk
from tkinter import ttk
from src.clear_main_frame import clear_main_frame
from controller.products.add_product import add_product
from controller.products.update_product import update_product
from controller.products.load_product_categories import load_product_categories
from controller.products.load_products import load_products
from controller.products.delete_product import delete_product


class ProductManagement:
    def __init__(self, root, main_frame, cursor, conn):
        self.root = root
        self.main_frame = main_frame
        self.cursor = cursor
        self.conn = conn
        self.products_data_list = []  # List to hold product data
        self.categories_data_dict = {}  # Dictionary to hold category data

    def show_products(self):
        """Show products management interface"""
        clear_main_frame(self.main_frame)

        # Title
        tk.Label(self.main_frame, text="Products Management",
                 font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

        # Form frame
        form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Product",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
        form_frame.pack(fill='x', pady=10)

        tk.Label(form_frame, text="Name:", bg='#f0f0f0').grid(
            row=0, column=0, sticky='w', padx=10, pady=5)
        self.item_name_entry = tk.Entry(form_frame, width=20)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Serial No:", bg='#f0f0f0').grid(
            row=0, column=2, sticky='w', padx=10, pady=5)
        self.item_serial_entry = tk.Entry(form_frame, width=20)
        self.item_serial_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Category:", bg='#f0f0f0').grid(
            row=1, column=0, sticky='w', padx=10, pady=5)
        self.item_category_combo = ttk.Combobox(form_frame, width=18)
        self.item_category_combo.grid(row=1, column=1, padx=10, pady=5)
        self.item_category_combo['state'] = 'readonly'

        tk.Label(form_frame, text="Price:", bg='#f0f0f0').grid(
            row=1, column=2, sticky='w', padx=10, pady=5)
        self.item_price_entry = tk.Entry(form_frame, width=20)
        self.item_price_entry.grid(row=1, column=3, padx=10, pady=5)

        # Third row
        tk.Label(form_frame, text="Total Quantity:", bg='#f0f0f0').grid(
            row=2, column=0, sticky='w', padx=10, pady=5)
        self.item_total_entry = tk.Entry(form_frame, width=20)
        self.item_total_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Available:", bg='#f0f0f0').grid(
            row=2, column=2, sticky='w', padx=10, pady=5)
        self.item_available_entry = tk.Entry(form_frame, width=20)
        self.item_available_entry.grid(row=2, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Available:", bg='#f0f0f0').grid(
            row=2, column=2, sticky='w', padx=10, pady=5)
        self.item_available_entry = tk.Entry(form_frame, width=20)
        self.item_available_entry.grid(row=2, column=3, padx=10, pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.grid(row=1, column=4, pady=10)

        self.add_button = tk.Button(button_frame, text="Add Product", command=lambda: add_product(self),
                                    bg='#27ae60', fg='white', padx=20)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(button_frame, text="Update Product", command=lambda: update_product(self),
                                       bg='#f39c12', fg='white', padx=20)

        tk.Button(button_frame, text="Clear", command=self.clear_product_form,
                  bg='#95a5a6', fg='white', padx=20).grid(row=0, column=2, padx=5)

        # List frame
        list_frame = tk.LabelFrame(self.main_frame, text="Products List",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, pady=10)

        # Treeview for products
        columns = ('ID', 'Name', 'Serial No', 'Category',
                   'Total', 'Available', 'Price')
        self.item_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.item_tree.heading(col, text=col)
            if col == 'ID':
                self.item_tree.column(col, width=0, stretch=False)
            else:
                self.item_tree.column(col, width=120)

        scrollbar2 = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.item_tree.yview)
        self.item_tree.configure(yscrollcommand=scrollbar2.set)

        self.item_tree.pack(side='left', fill='both', expand=True)
        scrollbar2.pack(side='right', fill='y')

        # Bind events
        self.item_tree.bind('<Double-1>', self.load_product_data)

        # Context menu
        self.item_menu = tk.Menu(self.root, tearoff=0)
        self.item_menu.add_command(
            label="Edit", command=self.load_product_data)
        self.item_menu.add_command(
            label="Delete", command=lambda: delete_product(self))
        self.item_tree.bind('<Button-3>', self.show_product_context_menu)

        load_product_categories(self)
        load_products(self)

    def show_add_button(self):
        """Show add button"""
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button.grid_forget()

    def show_update_button(self):
        """Show update button"""
        self.update_button.grid(row=0, column=0, padx=5)
        self.add_button.grid_forget()

    def clear_product_form(self):
        """Clear item form"""
        self.item_name_entry.delete(0, tk.END)
        self.item_serial_entry.delete(0, tk.END)
        self.item_category_combo.set('')
        self.item_total_entry.delete(0, tk.END)
        self.item_available_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)

        self.show_add_button()

    def load_product_data(self, event=None):
        """Load product data into form"""
        selected = self.item_tree.selection()

        if selected:
            self.show_update_button()

            item = self.item_tree.item(selected[0])
            values = item['values']

            self.item_name_entry.delete(0, tk.END)
            self.item_name_entry.insert(0, values[1])

            self.item_serial_entry.delete(0, tk.END)
            self.item_serial_entry.insert(0, values[2])

            self.item_category_combo.set(values[3])

            self.item_total_entry.delete(0, tk.END)
            self.item_total_entry.insert(0, values[4])

            self.item_available_entry.delete(0, tk.END)
            self.item_available_entry.insert(0, values[5])

            self.item_price_entry.delete(0, tk.END)
            self.item_price_entry.insert(0, values[6])

    def show_product_context_menu(self, event):
        self.item_menu.tk_popup(event.x_root, event.y_root)
