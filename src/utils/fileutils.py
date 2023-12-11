
"""
Utilities for dealing with files and directories
"""

import os.path
from pathlib import Path


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def ensure_dir_for_file(path):
    directory = os.path.dirname(path)
    if directory:
        ensure_dir(directory)


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


