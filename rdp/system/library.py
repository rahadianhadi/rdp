
def is_library_installed(library_name):
    """
    Check if a specific library is installed.

    :param library_name: The name of the library to check.
    :return: True if the library is installed, False otherwise.
    """
    try:
        __import__(library_name)
        return True
    except ImportError:
        return False