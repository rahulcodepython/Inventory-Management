from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.products import ProductManagement


def load_product_categories(self: "ProductManagement"):
    """Load categories for product form"""
    self.cursor.execute('SELECT id, name FROM categories ORDER BY name')
    categories = self.cursor.fetchall()

    combo_box_values = []
    for cat in categories:
        combo_box_values.append(cat[1])
        self.categories_data_dict[cat[1]] = cat[0]

    self.item_category_combo['values'] = combo_box_values
