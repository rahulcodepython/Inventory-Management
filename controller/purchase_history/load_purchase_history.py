from src.date_formatter import format_date
from typing import TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from ui.purchase_history import PurchaseHistoryManagement


def load_purchase_history(self: "PurchaseHistoryManagement"):
    """Load purchase history into treeview"""
    # if not self.history_items:
    self.cursor.execute('''
SELECT
    p.id AS purchase_id,
    c.name AS customer_name,
    c.mobile AS customer_mobile,
    p.total_amount AS total_amount,
    p.purchase_date,
    i.name AS product_name,
    pi.quantity,
    pi.unit_price,
    pi.total_price
FROM purchases p
JOIN customers c ON c.id = p.customer_id
JOIN purchase_items pi ON pi.purchase_id = p.id
JOIN items i ON i.id = pi.item_id
ORDER BY p.purchase_date DESC

    ''')
    rows = self.cursor.fetchall()

    purchases = defaultdict(lambda: {
        'name': '',
        'mobile': '',
        'date': '',
        'total_amount': 0.0,
        'items': []
    })

    for row in rows:
        purchase_id, name, mobile, total_amount, date, product, qty, unit_price, total_price = row
        purchases[purchase_id]['name'] = name
        purchases[purchase_id]['mobile'] = mobile
        purchases[purchase_id]['date'] = format_date(date)
        purchases[purchase_id]['total_amount'] = total_amount
        purchases[purchase_id]['items'].append(
            f"{product} x{qty} @{unit_price} = {total_price}"
        )

    return purchases
