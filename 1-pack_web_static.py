#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder

    Arguments:
        None
    Returns:
        (str) file path
    """
    dt = datetime.now()
    timestamps = "{}{}{}{}{}{}".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    fp = "versions/web_static_{}.tgz".format(timestamps)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(fp)).failed is True:
        return None
    return fp
