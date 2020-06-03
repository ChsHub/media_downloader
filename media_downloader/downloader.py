from os import makedirs

from os.path import exists, abspath, join


def create_user_dir(directory:str, user:str) -> str:
    """
    Create directory for storing videos and images
    :param directory: Directory path
    :param user: User name
    :return: New directory path
    """
    # Create directory for saving images
    if not exists(directory):
        raise OSError('Directory does not exist')
    user_dir = abspath(join(directory, user))
    if not exists(user_dir):
        makedirs(user_dir)
    return user_dir