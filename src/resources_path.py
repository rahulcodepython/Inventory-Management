import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource for dev and PyInstaller runtime """
    try:
        base_path = sys._MEIPASS  # Used by PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
