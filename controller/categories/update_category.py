from tkinter import messagebox


def update_category(cat_tree, cat_name_entry, cat_desc_entry, cursor, conn, categories_data_list, show_add_button, clear_category_form):
    """Update selected category"""
    selected = cat_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Please select a category to update!")
        return

    name = cat_name_entry.get().strip()
    description = cat_desc_entry.get().strip()

    if not name:
        messagebox.showerror("Error", "Category name is required!")
        return

    try:
        item = cat_tree.item(selected[0])
        index = cat_tree.index(selected[0])
        category_id = item['values'][0]

        cursor.execute('''
            UPDATE categories SET name = ?, description = ?
            WHERE id = ?
        ''', (name, description, category_id))
        conn.commit()
        messagebox.showinfo("Success", "Category updated successfully!")
        clear_category_form()

        updated_row = (category_id, name, description)
        categories_data_list[index] = updated_row
        cat_tree.item(selected[0], values=updated_row[1:])
        cat_tree.selection_remove(selected[0])

        show_add_button()  # Reset to add button after update
    except Exception as e:
        messagebox.showerror("Error", f"Error updating category: {str(e)}")
