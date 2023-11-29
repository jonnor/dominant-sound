
"""
Utilities for dealing with files and directories
"""

import os.path

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_dir_for_file(path):
    directory = os.path.dirname(path)
    if directory:
        ensure_dir(directory)


