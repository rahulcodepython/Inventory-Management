import tkinter as tk


def create_main_interface(root, main_frame, show_categories, show_products, show_customers):
    """Create the main interface with navigation"""
    # Header
    header_frame = tk.Frame(root, bg='#2c3e50', height=70)
    header_frame.pack(fill='x', padx=0, pady=0)
    header_frame.pack_propagate(False)

    title_label = tk.Label(header_frame, text="Inventory Management System",
                           font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
    title_label.pack(pady=10)

    # Navigation buttons
    nav_frame = tk.Frame(root, bg='#34495e', height=55)
    nav_frame.pack(fill='x')
    nav_frame.pack_propagate(False)

    button_style = {'font': ('Arial', 12), 'bg': '#3498db', 'fg': 'white',
                    'relief': 'flat', 'padx': 20, 'pady': 8}

    tk.Button(nav_frame, text="Categories", command=show_categories,
              **button_style).pack(side='left', padx=10, pady=10)
    tk.Button(nav_frame, text="Products", command=show_products,
              **button_style).pack(side='left', padx=10, pady=10)
    tk.Button(nav_frame, text="Customers", command=show_customers,
              **button_style).pack(side='left', padx=10, pady=10)

    # Main content area
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    show_categories()  # Show categories by default
