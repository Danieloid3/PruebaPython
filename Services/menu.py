# python
from Utils.Validator import *
from Services.Inventory import Inventory
from Services.UserService import UserService
from Services.SaleService import SaleService
from Utils.Decorator import *
from Models.User import User


def manageUsers(user_service: UserService) -> None:
    while True:
        try:
            print("\n--- Users Menu ---")
            print("1. Display Users")
            print("2. Search User")
            print("3. Add User")
            print("4. Update User")
            print("5. Save Users CSV")
            print("6. Back")
            opt = input("Choose an option: ").strip()

            match opt:
                case "1":
                    user_service.displayUsers()
                case "2":
                    query = input("Enter name, username or ID to search: ").strip()
                    user_service.searchUser(query)
                case "3":
                    print("Add User")
                    name = ""
                    while not is_valid_name(name):
                        name = input("Name: ").strip()
                        if not is_valid_name(name):
                            print("You have entered an invalid name")
                    username = ""
                    while not is_valid_name(username):
                        username = input("Username: ").strip()
                        if not is_valid_name(username):
                            print("You have entered an invalid username")
                    password = ""
                    while not is_non_empty_string(password):
                        password = input("Password: ").strip()
                        if not is_non_empty_string(password):
                            print("You have entered an invalid password")
                    role_in = ""
                    while role_in not in ("1", "2"):
                        role_in = input("Role (1=Admin, 2=Client): ").strip()
                        if role_in not in ("1", "2"):
                            print("You have entered an invalid role")
                    user_service.addUser(name, username, password, int(role_in))
                case "4":
                    print("Update User")
                    current_name = input("Enter current user name to update: ").strip()
                    new_name_in = input("New name [leave empty to keep]: ").strip()
                    new_username_in = input("New username [leave empty to keep]: ").strip()
                    new_password_in = input("New password [leave empty to keep]: ").strip()
                    role_in = ""
                    while role_in not in ("", "1", "2"):
                        role_in = input("New role (1=Admin, 2=Client) [empty to keep]: ").strip()
                        if role_in not in ("", "1", "2"):
                            print("You have entered an invalid role")
                    new_name_val = None if new_name_in == "" else new_name_in if is_valid_name(new_name_in) else None
                    if new_name_in != "" and new_name_val is None:
                        print(color("Invalid new name. Skipping name change.", "yellow"))
                    new_username_val = None if new_username_in == "" else new_username_in if is_valid_name(new_username_in) else None
                    if new_username_in != "" and new_username_val is None:
                        print(color("Invalid new username. Skipping username change.", "yellow"))
                    new_password_val = None if new_password_in == "" else new_password_in if is_non_empty_string(new_password_in) else None
                    if new_password_in != "" and new_password_val is None:
                        print(color("Invalid new password. Skipping password change.", "yellow"))
                    role_val = None if role_in == "" else int(role_in)
                    user_service.updateUser(
                        current_name,
                        new_name=new_name_val,
                        new_username=new_username_val,
                        new_password=new_password_val,
                        role=role_val
                    )
                case "5":
                    user_service.saveCSV("../Archivos/Users.csv")
                case "6":
                    print("Returning to Admin menu...")
                    break
                case _:
                    print("You have entered an invalid option")
        except ValueError:
            print("You have entered an invalid number")


def menuAdmin(inv: Inventory, user_service: UserService, sale_service: SaleService) -> None:
    while True:
        try:
            print("\nMenú:")
            print("1. Add Product")
            print("2. Search Product")
            print("3. Display Inventory")
            print("4. Update Product")
            print("5. Save Inventory CSV")
            print("6. Show Statistics")
            print("7. Manage Users")
            print("8. Display Sales")
            print("9. Save Sales CSV")
            print("10. Exit")
            menu = input("Choose an option: ").strip()

            match menu:
                case "1":
                    flag = True
                    while flag:
                        print("Add Product")
                        name = ""
                        while not is_valid_name(name):
                            name = input("Product name: ").strip()
                            if not is_valid_name(name):
                                print("You have entered an invalid name")
                        author = ""
                        while not is_valid_name(author):
                            author = input("Product author: ").strip()
                            if not is_valid_name(author):
                                print("You have entered an invalid author")
                        category = ""
                        while not is_valid_name(category):
                            category = input("Product category: ").strip()
                            if not is_valid_name(category):
                                print("You have entered an invalid category")
                        quantity = ""
                        while not is_positive_int_str(quantity):
                            quantity = input("Quantity: ").strip()
                            if not is_positive_int_str(quantity):
                                print("You have entered an invalid quantity")
                        price = ""
                        while not is_positive_decimal(price):
                            price = input("Price: ").strip()
                            if not is_positive_decimal(price):
                                print(color("You have entered an invalid price", "red"))
                        added = inv.addProduct(
                            name, author, category, int(quantity), float(price.replace(",", "."))
                        )
                        if not added:
                            upd = input("Do you want to update the existing item? (y/n): ").strip().lower()
                            if parse_bool(upd) is True:
                                product = inv.findProductByName(name)
                                if product:
                                    while True:
                                        new_name_in = input(f"New product name [{product.name}]: ").strip()
                                        if new_name_in == "" or is_valid_name(new_name_in):
                                            break
                                        print("You have entered an invalid name")
                                    while True:
                                        new_author_in = input(f"New product author [{product.author}]: ").strip()
                                        if new_author_in == "" or is_valid_name(new_author_in):
                                            break
                                        print("You have entered an invalid author")
                                    while True:
                                        new_category_in = input(f"New product category [{product.category}]: ").strip()
                                        if new_category_in == "" or is_valid_name(new_category_in):
                                            break
                                        print("You have entered an invalid category")
                                    while True:
                                        quantity_in = input(f"New Quantity [{product.quantity}]: ").strip()
                                        if quantity_in == "" or is_positive_int_str(quantity_in):
                                            break
                                        print("You have entered an invalid quantity")
                                    while True:
                                        price_in = input(f"New Price [{product.price}]: ").strip()
                                        if price_in == "" or is_valid_decimal(price_in):
                                            break
                                        print(color("You have entered an invalid price", "red"))
                                    new_name_val = None if new_name_in == "" else new_name_in
                                    new_author_val = None if new_author_in == "" else new_author_in
                                    new_category_val = None if new_category_in == "" else new_category_in
                                    quantity_val = None if quantity_in == "" else int(quantity_in)
                                    price_val = None if price_in == "" else float(price_in.replace(",", "."))
                                    inv.updateProduct(
                                        name, new_name_val, new_author_val, new_category_val, quantity_val, price_val
                                    )
                        inv.displayInventory()
                        cont = ""
                        while parse_bool(cont) not in (True, False):
                            cont = input("Do you want to add another product? (y/n): ").strip().lower()
                            if parse_bool(cont) not in (True, False):
                                print("You have entered an invalid option")
                        if parse_bool(cont) is False:
                            flag = False
                            print("Returning to main menu...")
                case "2":
                    print("Search Product")
                    query = input("Enter product name, author, category or ID to search: ").strip()
                    inv.searchProduct(query)
                case "3":
                    print("Display Inventory")
                    inv.displayInventory()
                case "4":
                    print("Update Product")
                    name = input("Enter product name to update: ").strip()
                    product = inv.findProductByName(name)
                    if product:
                        while True:
                            new_name_in = input(f"New product name [{product.name}]: ").strip()
                            if new_name_in == "" or is_valid_name(new_name_in):
                                break
                            print("You have entered an invalid name")
                        while True:
                            new_author_in = input(f"New product author [{product.author}]: ").strip()
                            if new_author_in == "" or is_valid_name(new_author_in):
                                break
                            print("You have entered an invalid author")
                        while True:
                            new_category_in = input(f"New product category [{product.category}]: ").strip()
                            if new_category_in == "" or is_valid_name(new_category_in):
                                break
                            print("You have entered an invalid category")
                        quantity_in = input(f"New Quantity [{product.quantity}]: ").strip()
                        while not (quantity_in == "" or is_positive_int_str(quantity_in)):
                            print("You have entered an invalid quantity")
                            quantity_in = input(f"New Quantity [{product.quantity}]: ").strip()
                        price_in = input(f"New Price [{product.price}]: ").strip()
                        while not (price_in == "" or is_valid_decimal(price_in)):
                            print(color("You have entered an invalid price", "red"))
                            price_in = input(f"New Price [{product.price}]: ").strip()
                        new_name_val = None if new_name_in == "" else new_name_in
                        new_author_val = None if new_author_in == "" else new_author_in
                        new_category_val = None if new_category_in == "" else new_category_in
                        quantity_val = None if quantity_in == "" else int(quantity_in)
                        price_val = None if price_in == "" else float(price_in.replace(",", "."))
                        inv.updateProduct(name, new_name_val, new_author_val, new_category_val, quantity_val, price_val)
                    else:
                        print(color("Product not found.", "red"))
                case "5":
                    print("Save Inventory CSV")
                    inv.saveCSV("../Archivos/Inventario.csv")
                case "6":
                    inv.displayStatistics()
                case "7":
                    manageUsers(user_service)
                case "8":
                    print("Display Sales")
                    sale_service.displaySales()
                    sale_service.displayStatistics()
                case "9":
                    print("Save Sales CSV")
                    sale_service.saveCSV("../Archivos/Sales.csv")
                case "10":
                    print("Exiting...")
                    break
                case _:
                    print("You have entered an invalid option")
        except ValueError:
            print("You have entered an invalid number")


def menuClient(inv: Inventory, sale_service: SaleService, current_user: User) -> None:
    while True:
        try:
            print("\nMenú:")
            print("1. Buy Product")
            print("2. Search Product")
            print("3. Exit")
            menu = input("Choose an option: ").strip()

            match menu:
                case "1":
                    print("Buy Product")
                    name = input("Enter product name to buy: ").strip()
                    product = inv.findProductByName(name)
                    if not product:
                        print(color("Product not found.", "red"))
                        continue
                    qty = ""
                    while not is_positive_int_str(qty):
                        qty = input(f"Quantity (available {product.quantity}): ").strip()
                        if not is_positive_int_str(qty):
                            print("You have entered an invalid quantity")
                    qty_i = int(qty)
                    if qty_i > product.quantity:
                        print(color("Insufficient stock.", "red"))
                        continue
                    product.quantity = product.quantity - qty_i
                    sale_service.addSale(
                        username=current_user.username,
                        product=product.name,
                        quantity=qty_i,
                        price=product.price,
                        role=int(current_user.role)
                    )
                    sale_service.saveCSV("../Archivos/Sales.csv", append=True)
                    inv.saveCSV("../Archivos/Inventario.csv")
                    inv.loadCSV("../Archivos/Inventario.csv")
                    print(color(f"Purchase successful. Total: ${product.price * qty_i:.2f}", "green"))
                case "2":
                    print("Search Product")
                    query = input("Enter product name, author, category or ID to search: ").strip()
                    inv.searchProduct(query)
                case "3":
                    print("Exiting...")
                    break
                case _:
                    print("You have entered an invalid option")
        except ValueError:
            print("You have entered an invalid number")


def login(user_service: UserService):
    max_tries = 3
    for attempt in range(1, max_tries + 1):
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        for u in user_service._users:
            if u.username == username and u.password == password:
                print(color("Login Successful", "green"))
                return u
        print(color(f"Invalid credentials. Attempt {attempt}/{max_tries}", "red"))
    print(color("Too many attempts. Bye.", "red"))
    return None


def main() -> None:
    inv = Inventory()
    user_service = UserService()
    sale_service = SaleService()

    filePathInventory = "../Archivos/Inventario.csv"
    filePathUser = "../Archivos/Users.csv"
    filePathSales = "../Archivos/Sales.csv"

    inv.loadCSV(filePathInventory)
    user_service.loadCSV(filePathUser)
    sale_service.loadCSV(filePathSales)

    u = login(user_service)
    if not u:
        return

    try:
        role = int(u.role)
    except Exception:
        role = 0

    if role == 1:
        menuAdmin(inv, user_service, sale_service)
    elif role == 2:
        menuClient(inv, sale_service, u)
    else:
        print(color("User role not recognized.", "red"))


if __name__ == "__main__":
    main()
