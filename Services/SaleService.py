# python
from Models.Sale import Sale
from Utils.Decorator import *
import csv
from pathlib import Path
from collections import Counter

class SaleService:
    def __init__(self):
        self._sales: list[Sale] = []

    def _next_id(self) -> int:
        return max((s.saleID for s in self._sales), default=0) + 1

    def addSale(self, username: str, product: str, quantity: int, price: float, role: int) -> Sale:
        sale = Sale(username=username, product=product, quantity=int(quantity), price=float(price), role=int(role), sale_id=self._next_id())
        self._sales.append(sale)
        print(color(f"Sale #{sale.saleID} registered for {username}: {quantity} x {product} (${price:.2f} c/u) -> Total ${sale.total:.2f}", "green"))
        return sale

    def displaySales(self):
        if not self._sales:
            print(color("There are no sales yet.", "yellow"))
            return
        print(color("Current Sales:", "blue"))
        for s in self._sales:
            print(f"ID: {s.saleID} | User: {s.username} | Product: {s.product} | Qty: {s.quantity} | Price: {s.price} | Total: {s.total}")
        print(color(f"Total sales count: {len(self._sales)}", "magenta"))

    def displayStatistics(self):
        if not self._sales:
            print(color("There are no sales. No statistics to show.", "yellow"))
            return
        total_revenue = sum(s.total for s in self._sales)
        total_items = sum(s.quantity for s in self._sales)
        by_product = Counter(s.product for s in self._sales)
        by_user = Counter(s.username for s in self._sales)
        top_products= by_product.most_common(3)
        top_users = by_user.most_common(3)
        print(top_products, top_users)

        print(color("--- Sales Statistics ---", "blue"))
        print(f"Total revenue: {color(f'${total_revenue:.2f}', 'green')}")
        print(f"Total items sold: {color(str(total_items), 'cyan')}")
        print("-" * 30)
        # print(f"Top product: {top_product.keys()[0]} ({color(str(top_product.values()[0]), 'yellow')} sales)")
        # print(f"Top buyer: {top_user} ({color(str(top_user.values()[0]), 'yellow')} purchases)")
        for product in top_products:
            print(f"Top product: {top_products.index(product)+1}. {product[0]}: {product[1]} sells")
        print(color("-" * 30, "magenta"))
        for client in top_users:
            print(f"Top client: {top_users.index(client)+1}. {client[0]}, with {client[1]} buys.")
        print(color("-----------------------", "blue"))

    def saveCSV(self, filePath: str, append: bool = False) -> None:
        path = Path(filePath)
        if path.suffix.lower() != ".csv":
            path.mkdir(parents=True, exist_ok=True)
            path = path / "Sales.csv"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        new_file = not path.exists()
        mode = "a" if append else "w"
        with path.open(mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new_file or not append:
                writer.writerow(["saleID", "username", "product", "quantity", "price", "role", "total"])
            for s in self._sales:
                writer.writerow([s.saleID, s.username, s.product, s.quantity, s.price, s.role, s.total])
        print(color(f"Sales saved to {str(path)}", "green"))

    def loadCSV(self, filePath: str) -> None:
        path = Path(filePath)
        if not path.is_file():
            print(color(f"No sales file found at '{filePath}'. Starting fresh.", "yellow"))
            return

        loaded_ids = set()
        try:
            with path.open(mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                try:
                    header = next(reader)
                except StopIteration:
                    print(color(f"Sales file '{filePath}' is empty.", "yellow"))
                    return

                self._sales.clear()
                for i, row in enumerate(reader, start=2):
                    if not row:
                        continue
                    if len(row) < 6:
                        print(color(f"Warning: Skipping malformed row {i} in '{filePath}'.", "yellow"))
                        continue
                    try:
                        sale_id = int(row[0])
                        if sale_id in loaded_ids:
                            print(color(f"Warning: Duplicate sale ID '{sale_id}' found in row {i}. Skipping.", "yellow"))
                            continue
                        username = str(row[1])
                        product = str(row[2])
                        quantity = int(row[3])
                        price = float(row[4])
                        role = int(row[5])
                        sale = Sale(username=username, product=product, quantity=quantity, price=price, role=role, sale_id=sale_id)
                        self._sales.append(sale)
                        loaded_ids.add(sale_id)
                    except (ValueError, IndexError) as conversion_error:
                        print(color(f"Warning: Could not parse row {i} in '{filePath}': {conversion_error}", "yellow"))

            if not self._sales and not loaded_ids:
                print(color(f"Sales file '{filePath}' has no valid sales to load.", "yellow"))
            else:
                print(color(f"Sales loaded successfully from '{filePath}'.", "green"))
        except Exception as e:
            print(color(f"Error loading sales from '{filePath}': {e}", "red"))
