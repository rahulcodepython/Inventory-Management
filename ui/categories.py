import tkinter as tk
from tkinter import ttk
from src.clear_main_frame import clear_main_frame
from controller.categories.add_category import add_category
from controller.categories.load_categories import load_categories
from controller.categories.delete_category import delete_category
from controller.categories.update_category import update_category


class CategoryManagement:
    def __init__(self, root, main_frame, cursor, conn):
        self.root = root
        self.main_frame = main_frame
        self.cursor = cursor
        self.conn = conn
        self.categories_data_list = []  # List to hold category data

    def show_categories(self):
        """Show categories management interface"""
        clear_main_frame(self.main_frame)

        # Title
        tk.Label(self.main_frame, text="Category Management",
                 font=('Arial', 18, 'bold'), bg='#f0f0f0').pack(pady=2)

        # Form frame
        form_frame = tk.LabelFrame(self.main_frame, text="Add/Edit Category",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=20, pady=10)
        form_frame.pack(fill='x', pady=10)

        # Form fields
        tk.Label(form_frame, text="Name:", bg='#f0f0f0').grid(
            row=0, column=0, sticky='w', pady=5)
        self.cat_name_entry = tk.Entry(form_frame, width=30)
        self.cat_name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(form_frame, text="Description:", bg='#f0f0f0').grid(
            row=0, column=2, sticky='w', pady=5)
        self.cat_desc_entry = tk.Entry(form_frame, width=30)
        self.cat_desc_entry.grid(row=0, column=3, pady=5, padx=10)

        # Buttons
        button_frame = tk.Frame(form_frame, bg='#f0f0f0')
        button_frame.grid(row=0, column=4, columnspan=2, pady=10)

        self.add_button = tk.Button(button_frame, text="Add Category", command=lambda: add_category(self),
                                    bg='#27ae60', fg='white', padx=20)
        self.add_button.grid(row=0, column=0, padx=5, sticky='w')

        self.update_button = tk.Button(button_frame, text="Update Category", command=lambda: update_category(self),
                                       bg='#f39c12', fg='white', padx=20)

        tk.Button(button_frame, text="Clear", command=self.clear_category_form,
                  bg='#95a5a6', fg='white', padx=20).grid(row=0, column=1, padx=5, sticky='w')

        # List frame
        list_frame = tk.LabelFrame(self.main_frame, text="Categories List",
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        list_frame.pack(fill='both', expand=True, pady=10)

        # Treeview for categories
        columns = ('ID', 'Name', 'Description')
        self.cat_tree = ttk.Treeview(
            list_frame, columns=columns, show='headings', height=10)

        for col in columns:
            self.cat_tree.heading(col, text=col)
            if col == 'ID':
                self.cat_tree.column(col, width=0, stretch=False)
            else:
                self.cat_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            list_frame, orient='vertical', command=self.cat_tree.yview)
        self.cat_tree.configure(yscrollcommand=scrollbar.set)

        self.cat_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Context menu
        self.cat_menu = tk.Menu(self.root, tearoff=0)
        self.cat_menu.add_command(
            label="Edit", command=self.load_category_data)
        self.cat_menu.add_command(
            label="Delete", command=lambda: delete_category(self))
        self.cat_tree.bind('<Button-3>', self.show_cat_context_menu)

        load_categories(self)

    def show_add_button(self):
        """Show Add button"""
        self.update_button.grid_forget()
        self.add_button.grid(row=0, column=0, padx=5, sticky='w')

    def show_update_button(self):
        """Show Update button"""
        self.add_button.grid_forget()
        self.update_button.grid(row=0, column=0, padx=5, sticky='w')

    def load_category_data(self, event=None):
        """Load category data into form"""
        selected = self.cat_tree.selection()
        if selected:
            self.show_update_button()

            item = self.cat_tree.item(selected[0])
            values = item['values']

            self.cat_name_entry.delete(0, tk.END)
            self.cat_name_entry.insert(0, values[1])

            self.cat_desc_entry.delete(0, tk.END)
            self.cat_desc_entry.insert(0, values[2])

    def show_cat_context_menu(self, event):
        """Show context menu for categories"""
        self.cat_menu.post(event.x_root, event.y_root)

    def clear_category_form(self):
        """Clear category form"""
        self.cat_name_entry.delete(0, tk.END)
        self.cat_desc_entry.delete(0, tk.END)
        self.cat_name_entry.focus_set()
        self.show_add_button()
