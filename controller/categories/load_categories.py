from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.categories import CategoryManagement


def load_categories(self: "CategoryManagement"):
    """Load categories into treeview"""
    for item in self.cat_tree.get_children():
        self.cat_tree.delete(item)

    if not self.categories_data_list:
        self.cursor.execute(
            'SELECT id, name, description FROM categories ORDER BY name')
        for row in self.cursor.fetchall():
            self.categories_data_list.append(row)
            self.cat_tree.insert('', 'end', values=row[1:])
    else:
        for row in self.categories_data_list:
            self.cat_tree.insert('', 'end', values=row[1:])
