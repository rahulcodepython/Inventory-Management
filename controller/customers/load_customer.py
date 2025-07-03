from typing import TYPE_CHECKING
from src.date_formatter import format_date

if TYPE_CHECKING:
    from ui.customers import CustomerManagement


def load_customers(self: "CustomerManagement"):
    """Load customers into treeview"""
    for item in self.cust_tree.get_children():
        self.cust_tree.delete(item)

    if not self.customer_data_list:
        self.cursor.execute(
            'SELECT id, name, mobile, created_at FROM customers ORDER BY name')
        for row in self.cursor.fetchall():
            row = (
                row[0],  # ID
                row[1],  # Name
                row[2],  # Mobile
                format_date(row[3])  # Created At
            )
            self.customer_data_list.append(row)
            self.cust_tree.insert('', 'end', values=row)

    else:
        for row in self.customer_data_list:
            self.cust_tree.insert('', 'end', values=row)
