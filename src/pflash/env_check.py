import os

def get_invocation_directory(rootdir: str):
    """Return the directory where the script was invoked."""
    if rootdir:
        return rootdir
    else:
        return os.getcwd()
