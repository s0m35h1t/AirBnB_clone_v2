#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["34.74.141.15", "34.73.24.78"]


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


def do_deploy(archive_path):
    """distributes an archive to your web servers

    Arguments:
        archive_path (str): path of the archive
    Returns:
        (bool) Returns False if the file at the path archive_path doesnt exist
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    fname = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(fname)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(fname)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, fname)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/"
           .format(fname, fname)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(fname)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(fname)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive"""
    fp = do_pack()
    if fp is None:
        return False
    return do_deploy(fp)
