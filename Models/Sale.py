# python
class Sale:
    __idActual = 1

    def __init__(self, username: str, product: str, quantity: int, price: float, role: int, sale_id: int | None = None):
        if sale_id is None:
            self._saleID = Sale.__idActual
            Sale.__idActual += 1
        else:
            self._saleID = int(sale_id)
            if self._saleID >= Sale.__idActual:
                Sale.__idActual = self._saleID + 1

        self._username = username
        self._product = product
        self._quantity = int(quantity)
        self._price = float(price)
        self._role = int(role)

    @property
    def saleID(self) -> int:
        return self._saleID

    @property
    def username(self) -> str:
        return self._username

    @property
    def product(self) -> str:
        return self._product

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = int(value)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = float(value)

    @property
    def role(self) -> int:
        return self._role

    @property
    def total(self) -> float:
        return self._price * self._quantity
