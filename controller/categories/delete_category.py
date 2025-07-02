from tkinter import messagebox


def delete_category(cat_tree, categories_data_list, cursor, conn):
    """Delete selected category"""
    selected = cat_tree.selection()

    if not selected:
        messagebox.showerror(
            "Error", "Please select a category to delete!")
        return

    if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
        try:
            index = cat_tree.index(selected[0])
            category_id = categories_data_list[index][0]

            cursor.execute(
                'DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            messagebox.showinfo(
                "Success", "Category deleted successfully!")

            categories_data_list.pop(index)
            cat_tree.delete(selected[0])
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error deleting category: {str(e)}")
