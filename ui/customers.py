import tkinter as tk
from tkinter import ttk
from src.clear_main_frame import clear_main_frame
from controller.customers.add_customer import add_customer
from controller.customers.update_customer import update_customer
from controller.customers.delete_customer import delete_customer
from controller.customers.load_customer import load_customers


class CustomerManagement:
    def __init__(self, root, main_frame, cursor, conn):
        self.root = root
        self.main_frame = main_frame
        self.cursor = cursor
        self.conn = conn
        self.customer_data_list = []

    def show_customers(self):
        """Show customers management interface"""
        clear_main_frame(self.main_frame)

        # Title
        tk.Label(self.main_frame, text="Customer Management",
                 font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=10)

        # Form frame
        form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Customer",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
        form_frame.pack(fill='x', pady=10)

        # Form fields
        tk.Label(form_frame, text="Name:", bg='#f0f0f0').grid(
            row=0, column=0, sticky='w', pady=5)
        self.cust_name_entry = tk.Entry(form_frame, width=30)
        self.cust_name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Mobile:", bg='#f0f0f0').grid(
            row=0, column=2, sticky='w', pady=5)
        self.cust_mobile_entry = tk.Entry(form_frame, width=30)
        self.cust_mobile_entry.grid(row=0, column=3, pady=5, padx=10)

        # Buttons
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.grid(row=0, column=4, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add Customer", command=lambda: add_customer(self),
                                    bg='#27ae60', fg='white', padx=20)
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button = tk.Button(button_frame, text="Update Customer", command=lambda: update_customer(self),
                                       bg='#f39c12', fg='white', padx=20)
        tk.Button(button_frame, text="Clear", command=self.clear_customer_form,
                  bg='#95a5a6', fg='white', padx=20).grid(row=0, column=1, padx=5)

        # List frame
        list_frame = tk.LabelFrame(self.main_frame, text="Customers List",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, pady=10)

        # Treeview for customers
        columns = ('ID', 'Name', 'Mobile', 'Joined At')
        self.cust_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.cust_tree.heading(col, text=col)
            if col == 'ID':
                self.cust_tree.column(col, width=0, stretch=False)
            else:
                self.cust_tree.column(col, width=120)

        scrollbar3 = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.cust_tree.yview)
        self.cust_tree.configure(yscrollcommand=scrollbar3.set)

        self.cust_tree.pack(side='left', fill='both', expand=True)
        scrollbar3.pack(side='right', fill='y')

        # Bind events
        self.cust_tree.bind('<Double-1>', self.load_customer_data)

        # Context menu
        self.cust_menu = tk.Menu(self.root, tearoff=0)
        self.cust_menu.add_command(
            label="Edit", command=self.load_customer_data)
        self.cust_menu.add_command(
            label="Delete", command=lambda: delete_customer(self))
        self.cust_tree.bind('<Button-3>', self.show_cust_context_menu)

        load_customers(self)

    def show_add_button(self):
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button.grid_forget()

    def show_update_button(self):
        self.update_button.grid(row=0, column=0, padx=5)
        self.add_button.grid_forget()

    def load_customer_data(self, event=None):
        """Load customer data into form"""
        selected = self.cust_tree.selection()

        if selected:
            self.show_update_button()
            item = self.cust_tree.item(selected[0])
            values = item['values']

            self.cust_name_entry.delete(0, tk.END)
            self.cust_name_entry.insert(0, values[1])

            self.cust_mobile_entry.delete(0, tk.END)
            self.cust_mobile_entry.insert(0, values[2])

    def clear_customer_form(self):
        """Clear customer form"""
        self.cust_name_entry.delete(0, tk.END)
        self.cust_mobile_entry.delete(0, tk.END)

        self.show_add_button()

    def show_cust_context_menu(self, event):
        self.cust_menu.tk_popup(event.x_root, event.y_root)
