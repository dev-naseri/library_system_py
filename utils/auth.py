import logging
from utils.database import Database
from utils.config import project_paths, set_current_user
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


logging.basicConfig(
    filename=project_paths.logs,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class AuthManager:
    """
    Manage Login and Register
    """

    def __init__(self):
        self.__ph = PasswordHasher()
        self.__db = Database()

    def hash_password(self, password):
        hashed_password = self.__ph.hash(password)
        return hashed_password

    def decode_password(self, hashed_password, password):
        try:
            self.__ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False

    def valid_input(self, inp, inp_is="username"):
        """Validates user input's"""

        if not inp:
            return self.valid_input(input(f"Please enter a valid {inp_is}: ")
                                    , inp_is)
        return inp

    def login(self, username=None, password=None):
        """Check username/password combination in database
        if it exists, return username"""

        if not username or not password:
            username = self.valid_input(input("Please enter a username: "))
            password = self.valid_input(input("Please enter a password: "),
                                        "password")

        result = self.__db.login(username)

        if not result:
            return None
        
        stored_username, stored_hashed_password = result
        is_currect = self.decode_password(stored_hashed_password, password)
        
        if is_currect:
            set_current_user(stored_username)
            return stored_username

    def create_user(self, username=None, password=None):
        """Create a new account in library system"""

        if username is None and password is None:
            username = self.valid_input(input("Please enter a username: "))
            password = self.valid_input(input("Please enter a password: "),
                                        "password")

        action = False
        hashed_password = self.hash_password(password)
        result = self.__db.create_user(username, hashed_password)
        if not result:
            logger.info(f"username: '{username}' is exists in library.")
        elif result == 1:
            logger.info(
                f"An account for '{username}' is created in library successfully."
            )
            set_current_user(username)
            return True
        elif result == -1:
            logger.info(f"An account with username: '{username}' is already registered.")

        return action