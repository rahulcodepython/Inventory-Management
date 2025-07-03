from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.products import ProductManagement


def load_products(self: "ProductManagement"):
    """Load items into treeview"""
    for item in self.item_tree.get_children():
        self.item_tree.delete(item)

    if not self.products_data_list:
        self.cursor.execute('''
            SELECT i.id, i.name, i.serial_no, c.name, i.total_amount, i.available_amount, i.price
            FROM items i
            LEFT JOIN categories c ON i.category_id = c.id
            ORDER BY i.name
        ''')
        for row in self.cursor.fetchall():
            self.products_data_list.append(row)
            self.item_tree.insert('', 'end', values=row)

    else:
        for row in self.products_data_list:
            self.item_tree.insert('', 'end', values=row)
