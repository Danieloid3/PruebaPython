# Services/UserService.py
from Models.User import User
from Utils.Decorator import *
import csv
from pathlib import Path

class UserService:
    def __init__(self):
        # Roles como enteros y IDs fijos para ejemplo
        self._users = [
            User("Daniela García", "Danieloide", "Danieloide", 1, 1),
            User("Andrés David", "Andres", "Andres", 2, 2),
        ]

    def userExists(self, name: str) -> bool:
        return self.findUserByName(name) is not None

    def _next_id(self) -> int:
        return max((u.userID for u in self._users), default=0) + 1

    def addUser(self, name: str, username: str, password: str, role: int) -> bool:
        if self.userExists(name):
            print(color("User already exists.", "red"))
            return False
        uid = self._next_id()
        user = User(name, username, password, role, user_id=uid)
        self._users.append(user)
        print(color(f"User {user.name} added successfully.", "green"))
        return True

    def findUserByName(self, name: str) -> User | None:
        for user in self._users:
            if user.name.lower() == name.lower():
                return user
        return None

    def searchUser(self, query: str) -> User | None:
        parcial = []
        for user in self._users:
            if query.lower() in user.name.lower() or str(user.userID) == query or query.lower() in user.username.lower():
                parcial.append(user)
        if parcial:
            print(color("Search Results:", "blue"))
            for user in parcial:
                print(f"ID: {user.userID} | Name: {user.name} | Username: {user.username} | Role: {user.role} ")
            return
        print(color("User not found.", "red"))
        return None


    def displayUsers(self):
        if not self._users:
            print(color("There are not users", "yellow"))
        else:
            count = len(self._users)
            print(color("Current Users:", "blue"))
            for user in self._users:
                print(f"ID: {user.userID} | Name: {user.name} | Username: {user.username} | Role: {user.role} ")
            print(color(f"Users in inventory: {count}", "magenta"))

    def updateUser(self, name: str,
                   new_name: str | None = None,
                   new_username: str | None = None,
                   new_password: str | None = None,
                   role: int | None = None):
        user = self.findUserByName(name)
        if not user:
            print(color("User not found.", "red"))
            return False
        if new_name is not None and new_name.strip() != "":
            user.name = new_name
        if new_username is not None and new_username.strip() != "":
            user.username = new_username
        if new_password is not None and new_password.strip() != "":
            user.password = new_password
        if role is not None:
            user.role = role

        print(color(f"User {user.name} updated successfully.", "green"))
        return True

    def saveCSV(self, filePath: str, append: bool = False) -> None:
        path = Path(filePath)
        # Fix: usar nombre por defecto `Users.csv` si se pasa un directorio
        if path.suffix.lower() != ".csv":
            path.mkdir(parents=True, exist_ok=True)
            path = path / "Users.csv"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
        new_file = not path.exists()
        mode = "a" if append else "w"
        with path.open(mode, newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new_file or not append:
                writer.writerow(["userID", "name", "username", "password", "role"])
            for u in self._users:
                writer.writerow([u.userID, u.name, u.username, u.password, u.role])
        print(color(f"Users saved to {str(path)}", "green"))

    def loadCSV(self, filePath: str) -> None:
        path = Path(filePath)
        if not path.is_file():
            print(color(f"No users file found at '{filePath}'. Starting fresh.", "yellow"))
            return

        loaded_ids = set()
        try:
            with path.open(mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                try:
                    header = next(reader)
                except StopIteration:
                    print(color(f"Users file '{filePath}' is empty.", "yellow"))
                    return

                self._users.clear()
                for i, row in enumerate(reader, start=2):
                    if not row:
                        continue
                    if len(row) != 5:
                        print(color(f"Warning: Skipping malformed row {i} (wrong number of columns) in '{filePath}'.", "yellow"))
                        continue
                    try:
                        user_id = int(row[0])
                        if user_id in loaded_ids:
                            print(color(f"Warning: Duplicate product ID '{user_id}' found in row {i}. Skipping.", "yellow"))
                            continue
                        user = User(
                            user_id=user_id,
                            name=str(row[1]),
                            username=str(row[2]),
                            password=str(row[3]),
                            role=int(row[4])
                        )
                        self._users.append(user)
                        loaded_ids.add(user_id)
                    except (ValueError, IndexError) as conversion_error:
                        print(color(f"Warning: Could not parse row {i} in '{filePath}': {conversion_error}", "yellow"))

            if not self._users and not loaded_ids:
                print(color(f"User file '{filePath}' has no valid products to load.", "yellow"))
            else:
                print(color(f"User loaded successfully from '{filePath}'.", "green"))
        except Exception as e:
            print(color(f"Error loading inventory from '{filePath}': {e}", "red"))


