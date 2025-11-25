"""
Configuration module for "Library System"


This module defines the main system paths and global project-level configuration
variables. The main purpose is to provide a central reference for file paths and
settings that other modules depend on.

Important variables:
--------------------------------------------------------------------------------
BASE_DIR (Path): The absolute path to the project root directory (the folder
where `main.py` is located).
--------------------------------------------------------------------------------
DATA_DIR (Path): The path to the data storage directory (usually
`{BASE_DIR}/data`).
--------------------------------------------------------------------------------
DATABASE_PATH (Path): The full path to the SQLite database file.
--------------------------------------------------------------------------------


How to use in other modules:
   - from utils.config import DATABASE_PATH
   - import sqlit
   - conn = sqlite3.connect(DATABASE_PATH)

Note:
- This file should not contain complex logic or functions.
- To change the paths, edit the variables in this module directly.
"""
import os
from pathlib import Path


class ProjectPath:
    def __init__(self, base, logs, db_path):
        self.base = base
        self.logs = logs
        self.db_path = db_path


BASE_DIR = Path(__file__).resolve().parent.parent

# Create data directory if not existed
DATA_DIR = BASE_DIR / 'data'
os.makedirs(DATA_DIR, exist_ok=True)


DATABASE_PATH = DATA_DIR / 'database.db'

# Log File Path
LOG_FILE = BASE_DIR / 'logs' / 'project.log'


project_paths = ProjectPath(
    base=BASE_DIR,  # Project Base Folder Path
    logs=LOG_FILE,
    db_path=DATABASE_PATH  # Database Path
)


# Global variable for current active user in library system
_current_user = None


def set_current_user(username):
    global _current_user
    _current_user = username


def get_current_user():
    return _current_user


def logout_user():
    global _current_user
    _current_user = None
