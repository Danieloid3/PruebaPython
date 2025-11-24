from Models.Product import Product
from Utils.Decorator import *
import csv
from pathlib import Path


class Inventory:
    def __init__(self):
        self._products = []

    def productExists(self, name: str) -> bool:
        return self.findProductByName(name) is not None

    def _next_id(self) -> int:
        return max((p.productID for p in self._products), default=0) + 1


    def addProduct(self, name: str, author: str, category: str, quantity: int, price: float) -> bool:
        if self.productExists(name):
            print(color("Item already exists.", "red"))
            return False
        pid = self._next_id()
        product = Product(name, author, category, quantity, price, product_id=pid)
        self._products.append(product)
        print(color(f"Product {product.name} added successfully.", "green"))
        return True

    def findProductByName(self, name: str) -> Product | None:
        for product in self._products:
            if product.name.lower() == name.lower():
                return product
        return None

    def searchProduct(self, query: str) -> Product | None:
        parcial = []
        for product in self._products:
            if query.lower() in product.name.lower()  or str(product.productID) == query or query.lower() in product.author.lower() or query.lower() in product.category.lower():
                parcial.append(product)
        if parcial:
            print(color ("Search Results:", "blue"))
            for product in parcial:
                print(f"ID: {product.productID} | Name: {product.name} | Quantity: {product.quantity} | Price: {product.price} | Total: {product.total}")
            return
        print(color("Product not found.", "red"))
        return None



    def displayInventory(self):
        if not self._products:
            print(color("Inventory is empty.", "yellow"))
        else:
            count = len(self._products)
            print(color("Current Inventory:", "blue"))
            for product in self._products:
                print(f"ID: {product.productID} | Name: {product.name} | Author: {product.author} | Category: {product.category} | Quantity: {product.quantity} | Price: {product.price} | Total: {product.total}")
            print(color(f"Products in inventory: {count}", "magenta"))

    def updateProduct(self, name: str,
                      new_name: str | None = None,
                      new_author: str | None = None,
                      new_category: str | None = None,
                      quantity: int | None = None,
                      price: float | None = None) -> bool:

        product = self.findProductByName(name)
        if not product:
            print(color("Product not found.", "red"))
            return False
        if new_name is not None and new_name.strip() != "":
            product.name = new_name
        if new_author is not None and new_author.strip() != "":
            product.author = new_author
        if new_category is not None and new_category.strip() != "":
            product.category = new_category
        if quantity is not None:
            product.quantity = quantity
        if price is not None:
            product.price = price
        print(color(f"Product {product.name} updated successfully.", "green"))
        return True

    def saveCSV(self, filePath: str, append: bool = False) -> None:
        path = Path(filePath)
        # Si se pasa solo un directorio (sin .csv) crear y usar nombre por defecto
        if path.suffix.lower() != ".csv":
            path.mkdir(parents=True, exist_ok=True)
            path = path / "Inventario.csv"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not path.exists()
        mode = "a" if append else "w"
        with path.open(mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new_file or not append:
                writer.writerow(["productID", "name", "author", "category", "quantity", "price", "total"])
            for p in self._products:
                writer.writerow([p.productID, p.name, p.author, p.category, p.quantity, p.price, p.total])
        print(color(f"Inventory saved to {str(path)}", "green"))


    def displayStatistics(self) -> None:
        if not self._products:
            print(color("Inventory is empty. No statistics to show.", "yellow"))
            return

        num_products = len(self._products)
        total_value = sum(p.total for p in self._products)

        most_expensive = max(self._products, key=lambda p: p.price)
        least_expensive = min(self._products, key=lambda p: p.price)
        most_stock = max(self._products, key=lambda p: p.quantity)
        least_stock = min(self._products, key=lambda p: p.quantity)

        print(color("--- Inventory Statistics ---", "blue"))
        print(f"Total number of unique products: {color(str(num_products), 'magenta')}")
        print(f"Total inventory value: {color(f'${total_value:.2f}', 'green')}")
        print("-" * 30)
        print("Most Expensive Product:")
        print(f"  - {most_expensive.name} ({color(f'${most_expensive.price:.2f}', 'yellow')})")
        print("Least Expensive Product:")
        print(f"  - {least_expensive.name} ({color(f'${least_expensive.price:.2f}', 'yellow')})")
        print("-" * 30)
        print("Product with Most Stock:")
        print(f"  - {most_stock.name} ({color(f'{most_stock.quantity} units', 'cyan')})")
        print("Product with Least Stock:")
        print(f"  - {least_stock.name} ({color(f'{least_stock.quantity} units', 'cyan')})")
        print(color("----------------------------", "blue"))

    def loadCSV(self, filePath: str) -> None:
        path = Path(filePath)
        if not path.is_file():
            print(color(f"No inventory file found at '{filePath}'. Starting fresh.", "yellow"))
            return

        loaded_ids = set()  # Conjunto para rastrear IDs ya cargados
        try:
            with path.open(mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                try:
                    header = next(reader)  # Omitir la cabecera
                except StopIteration:
                    print(color(f"Inventory file '{filePath}' is empty.", "yellow"))
                    return

                self._products.clear()  # Limpiar el inventario actual antes de cargar
                for i, row in enumerate(reader, start=2):  # Empezar a contar desde la línea 2
                    if not row:
                        continue  # Ignorar filas completamente vacías

                    if len(row) != 7:
                        print(
                            color(f"Warning: Skipping malformed row {i} (wrong number of columns) in '{filePath}'.",
                                  "yellow"))
                        continue

                    try:
                        product_id = int(row[0])
                        if product_id in loaded_ids:
                            print(color(f"Warning: Duplicate product ID '{product_id}' found in row {i}. Skipping.",
                                        "yellow"))
                            continue
                        product = Product(
                            product_id=product_id,
                            name=str(row[1]),
                            author=str(row[2]),
                            category=str(row[3]),
                            quantity=int(row[4]),
                            price=float(row[5])
                        )
                        self._products.append(product)
                        loaded_ids.add(product_id)  # Añadir el ID al conjunto de IDs cargados

                    except (ValueError, IndexError) as conversion_error:
                        print(color(f"Warning: Could not parse row {i} in '{filePath}': {conversion_error}",
                                    "yellow"))

            if not self._products and not loaded_ids:
                print(color(f"Inventory file '{filePath}' has no valid products to load.", "yellow"))
            else:
                print(color(f"Inventory loaded successfully from '{filePath}'.", "green"))

        except Exception as e:
            print(color(f"Error loading inventory from '{filePath}': {e}", "red"))