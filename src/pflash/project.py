"""
This module checks environment conditions
"""

import os


def get_inv_directory(rootdir: str):
    """Return the directory where the script was invoked."""
    if rootdir:
        return rootdir

    return os.getcwd()
