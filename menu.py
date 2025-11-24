# Producto Título autor, categoríía, precio
#cantidad en stock
#Registrar consultar, actualizar y eliminar

from Utils import *
from Utils.Validator import *
from Utils.Decorator import  *
from Inventory import *
inv = Inventory()
filePath = "Archivos/Inventario.csv"
inv.loadCSV(filePath)

while True:

    try:
        print("\nMenú:")
        print("1. Add Product")
        print("2. Search Product")
        print("3. display Inventory")
        print("4. update Product")
        print("5. Save CSV file")
        print("6. Show Statistics")
        print("7. Exit")
        menu = input("Choose an option: ")

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
                    quantity = -1
                    while not is_positive_int_str(quantity):
                        quantity = (input("Quantity: "))
                        if not is_positive_int_str(quantity):
                            print("You have entered an invalid quantity")

                    price = -1.0
                    while not is_positive_decimal(price):
                        price = (input("Price: "))
                        if not is_positive_decimal(price):
                            print(color("You have entered an invalid price", "red"))

                    added = inv.addProduct(name, int(quantity), float(price))
                    if not added:
                        upd =input("Do you want to update the existing item? (y/n): ").strip().lower()
                        if parse_bool(upd) is True:
                            product = inv.findProductByName(name)
                            while True:
                                new_name_in = input(f"New product name [{product.name}]: ").strip()
                                if new_name_in == "" or is_valid_name(new_name_in):
                                    break
                                print("You have entered an invalid name")

                            while True:
                                quantity_in = input(f"New Quantity [{product.quantity}]: ").strip()
                                if quantity_in == "" or is_positive_int_str(quantity_in):
                                    break
                                print("You have entered an invalid quantity")

                            while True:
                                price_in = input(f"New Price [{product.price}]: ").strip()
                                if price_in == "" or is_positive_decimal(price_in):
                                    break
                                print(color("You have entered an invalid price", "red"))

                            new_name_val = None if new_name_in == "" else new_name_in
                            quantity_val = None if quantity_in == "" else int(quantity_in)
                            price_val = None if price_in == "" else float(price_in)

                            inv.updateProduct(name, new_name_val, quantity_val, price_val)
                    inv.displayInventory()
                    cont = ""
                    while parse_bool(cont) != True and parse_bool(cont) != False:
                        cont = input("Do you want to add another product? (y/n): ").strip().lower()
                        if parse_bool(cont) != True and parse_bool(cont) != False:
                            print("You have entered an invalid option")
                        if parse_bool(cont) == False:
                            flag = False
                            print("Returning to main menu...")
                        else:
                            flag = True



            case "2":
                print("Search Product")
                name = input("Enter product name or ID to search: ").strip()
                inv.searchProduct(name)
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
                        quantity_in = input(f"New Quantity [{product.quantity}]: ").strip()
                        if quantity_in == "" or is_positive_int_str(quantity_in):
                            break
                        print("You have entered an invalid quantity")


                    while True:
                        price_in = input(f"New Price [{product.price}]: ").strip()
                        if price_in == "" or is_positive_decimal(price_in):
                            break
                        print(color("You have entered an invalid price", "red"))

                    new_name_val = None if new_name_in == "" else new_name_in
                    quantity_val = None if quantity_in == "" else int(quantity_in)
                    price_val = None if price_in == "" else float(price_in)

                    inv.updateProduct(name, new_name_val, quantity_val, price_val)
                else:
                    print(color("Product not found.", "red"))

            case "5":
                print("Save CSV file")
                inv.saveCSV(filePath)

            case "6":
                inv.displayStatistics()

            case "7":
                print("Exiting...")
                break
            case _:
                print("You have entered an invalid option")


    except ValueError:
        print("You have entered an invalid number")