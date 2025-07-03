from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.purchases import PurchaseManagement


def update_purchase_total(self: "PurchaseManagement"):
    """Update total purchase amount"""
    total = sum(item['total_price'] for item in self.purchase_items)
    self.total_label.config(text=f"{total:.2f}")
