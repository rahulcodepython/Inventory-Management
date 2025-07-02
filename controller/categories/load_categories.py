def load_categories(cat_tree, cursor, categories_data_list):
    """Load categories into treeview"""
    for item in cat_tree.get_children():
        cat_tree.delete(item)

    if not categories_data_list:
        cursor.execute(
            'SELECT id, name, description FROM categories ORDER BY name')
        for row in cursor.fetchall():
            categories_data_list.append(row)
            cat_tree.insert('', 'end', values=row[1:])
    else:
        for row in categories_data_list:
            cat_tree.insert('', 'end', values=row[1:])
