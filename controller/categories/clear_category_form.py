import tkinter as tk


def clear_category_form(cat_name_entry, cat_desc_entry, show_add_button):
    """Clear category form"""
    cat_name_entry.delete(0, tk.END)
    cat_desc_entry.delete(0, tk.END)
    cat_name_entry.focus_set()
    show_add_button()
