"""
DATABASE Relation's in project
"""
import logging
import sqlite3
from utils.config import project_paths


logging.basicConfig(
    filename=project_paths.logs,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


# Database Connector
class DatabaseConnector:
    """
    Create Connection to the database with two method
    """

    def __init__(self, path=project_paths.db_path):
        self._path = path
        self._conn = None
        self._cur = None

    def __enter__(self):
        """
        Create a Connection to Database
        if Connection succed Return: Conn, Cur -> tuple
        if not Return: False
        """

        try:
            self._conn = sqlite3.connect(self._path)
            self._cur = self._conn.cursor()
            logger.info("Connected to Database.")
            return (self._conn, self._cur)
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")

    def __exit__(self, exc_type, exc_val, traceback):
        """
        Disconnect from database.
        Always closes connection even if an exception occurs.
        Logs any exception.
        """
        try:
            if self._conn:
                self._conn.close()
                logger.info("Closing Connection to database")
        except sqlite3.Error as e:
            logger.error(f"Error closing database: {e}")

        if exc_type:
            logger.error(f"Exception occurred: {exc_type}: {exc_val}")
            # return None or False → exception will be propagated
            return False


class Database(DatabaseConnector):
    """
    Database Communication Class
    """
    
    def test(self):
        with self as (conn, cur):
            if conn:
                print(conn)
            if cur:
                print(cur)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        """
        Create Required Table's if not exists
        """

        with self as (conn, cursor):
            # Create users table if not exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                "username"	TEXT NOT NULL UNIQUE,
                                "password"	TEXT NOT NULL,
                                PRIMARY KEY("username")
                            );
                        ''')

            # Create books table if not exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                "book_id" INTEGER NOT NULL UNIQUE,
                                "title"	TEXT NOT NULL UNIQUE,
                                "author" TEXT NOT NULL,
                                "year" INTEGER NOT NULL,
                                "translator" TEXT,
                                "publisher" TEXT,
                                "owner"	TEXT NOT NULL,
                                PRIMARY KEY("book_id" AUTOINCREMENT)
                                FOREIGN KEY ("owner") REFERENCES users("username")
                            );
                        ''')

            conn.commit()

    def login(self, username):
        """Check user exists in database"""

        with self as (_, cursor):
            try:
                cursor.execute(
                    "SELECT * FROM users WHERE username = ?;",
                    (username,)
                )

                result = cursor.fetchone()

                if not result:
                    logger.info("No username and password found in database.")
                    return None

                logger.info(f"Username '{username}' found in database.")
                return result
            except sqlite3.Error as e:
                logger.error(f"Login failed: {e}")

    def check_username(self, username):
        """Check username exists in database"""
        with self as (_, cursor):
            try:
                cursor.execute(
                    "SELECT username FROM users \
                    WHERE username = ?;",
                    (username,)
                )

                result = cursor.fetchone()

                if not result:
                    logger.info("No username and password found in database.")
                    return None

                logger.info(f"Username '{username}' found in database.")
                return username
            except sqlite3.Error as e:
                logger.error(f"Login failed: {e}")
        

    def create_user(self, username, password):
        """
        Create new account in database
        """
        with self as (conn, cursor):
            try:
                if self.check_username(username):
                    logger.info(f"Username: {username} already exists.")
                    return 0

                cursor.execute(
                    "INSERT INTO users VALUES (?, ?);",
                    (username, password)
                )
                conn.commit()
                logger.info(f"New user '{username} added to database.")
                return 1

            except sqlite3.Error:
                logger.error("Failed to create new account.")
                return -1

    def add_book(
        self, title, author, year, owner, translator=None, publisher=None
    ):
        """
        Add new book to the database
        """
        with self as (conn, cursor):
            try:
                statement = """INSERT INTO books
                            (title, author, year, translator, publisher, owner)
                    SELECT ?, ?, ?, ?, ?, ?
                    WHERE NOT EXISTS (
                        SELECT 1 FROM books
                        WHERE title = ? AND author = ?
                    );
                """
                data_tuple = (
                    title, author, year, translator, publisher, owner, title,
                    author
                )
                cursor.execute(statement, data_tuple)
                conn.commit()
                logger.info(f"new book added to database: {title}:{author}")
                return True
            except sqlite3.Error as e:
                logger.error(f"ERROR ADDING BOOK: {e}")
                return False

    def update_book(
        self, title, author, new_title=None, new_author=None, new_year=None,
        new_translator=None, new_publisher=None, new_owner=None
    ):
        """
        Update a book in the database
        """
        with self as (conn, cursor):
            try:
                fields = []
                params = []

                if new_title is not None:
                    fields.append("title = ?")
                    params.append(new_title)
                if new_author is not None:
                    fields.append("author = ?")
                    params.append(new_author)
                if new_year is not None:
                    fields.append("year = ?")
                    params.append(new_year)
                if new_translator is not None:
                    fields.append("translator = ?")
                    params.append(new_translator)
                if new_publisher is not None:
                    fields.append("publisher = ?")
                    params.append(new_publisher)
                if new_owner is not None:
                    fields.append("owner = ?")
                    params.append(new_owner)

                if not fields:
                    logger.info("No input were givven to update book in database.")
                    return False

                params.append(title)
                params.append(author)

                statement = (f"UPDATE books SET {', '.join(fields)} "
                            f"WHERE title=? AND author=?")

                cursor.execute(statement, params)
                conn.commit()
                
                logger.info(f"Book {title} updated to {new_title}.")
                return True
            except sqlite3.Error as e:
                logger.error(f"ERROR RENAME BOOK: {e}")
                return False
    
    def delete_book(self, title, author):
        """Delete a book in the database"""
        with self as (conn, cursor):
            try:
                statement = (f"DELETE FROM books WHERE title=? AND author=?")
                cursor.execute(statement, (title, author))
                conn.commit()
                logger.info(f"Book: {title}:{author} delete from database.")
                return True
            except sqlite3.Error as e:
                logger.error(f"ERROR DELETE BOOK: {e}")
                return False
            

    def fetch_books(self, owner):
        """Return all books in the database"""
        with self as (_, cursor):
            try:
                statement = (f"SELECT * FROM books WHERE owner=?")
                cursor.execute(statement, (owner,))
                books = cursor.fetchall()
                
                if books:
                    logger.info(f"{owner} books fetched from database")
                    return books
                
                logger.info(f"{owner} has no book in database")
                return False
            except sqlite3.Error as e:
                logger.error(f"ERROR READ BOOKS: {e}")
                return False
