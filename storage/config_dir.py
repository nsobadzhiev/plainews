import os


def create_config_dir() -> bool:
    """
    Creates a directory for the application in the user home
    (os-independent)
    :return True, if a directory was created, otherwise False
    """
    config_dir = os.path.expanduser('~/.plainews/')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
        return True
    else:
        return False
