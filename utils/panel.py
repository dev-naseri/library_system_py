"""
Library System user interface
"""
from utils.auth import AuthManager
from utils.database import Database
from utils.config import get_current_user, set_current_user, logout_user


class Panel:
    def __init__(self):
        self.__db = Database()
        self.__manager = AuthManager()

    def signing_panel(self):
        """Signing interface"""
        ask = input("You have an Account: [y/n]? ")

        if ask.lower() not in ["y", "ye", "yes", "n", "no"]:
            return self.signing_panel()

        print("Please enter username and password:")

        username = input("Username:  ")
        password = input("Password:  ")

        if ask.lower() in ['y', 'ye', 'yes']:
            action = self.__manager.login(username, password)

            if action:
                print(f"Signing with '{action}'")
                set_current_user(username)
                return 1
            else:
                print("Login Failed")

        elif ask.lower() in ['n', 'no']:
            create = self.__manager.create_user(username, password)
            if create:
                print(f"Created new user and signing with: '{username}'")
                return 1
            if not create:
                print("Creating account failed")
        return self.signing_panel()

    def system_panel(self):
        """Library System user interface"""

        def valid_option(inp):
            if inp not in ["1", "2", "3", "4", "5", "6"]:
                return valid_option(input("Enter a valid option: "))
            return inp

        msgs = [
            f" Welcome to Library System '{get_current_user()}' ",
            " What would you like to do? ",
            " Here are your options: ",
            " 1) ADD New Book. ",
            f" 2) View '{get_current_user()}' books. ",
            " 3) Rename a book fields. ",
            " 4) Delete a book. ",
            " 5) SignOut Your Account. ",
            " 6) Exit. "
        ]
        for msg in msgs:
            print(msg.center(80, "*"))

        ask = valid_option(input("> Enter option: "))

        # Add new book to the library
        if ask == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            year = input("Enter book year: ")
            translator = input("Enter book translator: ")
            publisher = input("Enter book publisher: ")
            owner = get_current_user()
            self.__db.add_book(title=title, author=author, year=year,
                        translator=translator, publisher=publisher, owner=owner)


        # Print books of current active user
        if ask == "2":
            books = self.__db.fetch_books(get_current_user())
            for book in books:
                book_id, title, author, year, translator, publisher, owner = book
                print(f"Book ID: {book_id}")
                print(f"Title: {title}")
                print(f"Author: {author}")
                print(f"Year: {year}")
                print(f"Translator: {translator}")
                print(f"Publisher: {publisher}")
                print(f"Owner: {owner}")
                print("-" * 30)


        # update a book in library database
        if ask == "3":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            new_title = input("Enter new book title: ")
            new_author = input("Enter new book author: ")
            new_year = input("Enter new book year: ")
            new_translator = input("Enter new book translator: ")
            new_publisher = input("Enter new book publisher: ")
            new_owner = get_current_user()
            self.__db.update_book(title=title, author=author, new_title=new_title,
                            new_author=new_author, new_year=new_year,
                            new_translator=new_translator,
                            new_publisher=new_publisher,
                            new_owner=new_owner)

        if ask == "4":
            print("4 is here")
            t = input("Enter book title: ")
            a = input("Enter book author: ")
            self.__db.delete_book(t, a)

        if ask == "5":
            logout_user()

        if ask == "6":
            return 0

        return 1
