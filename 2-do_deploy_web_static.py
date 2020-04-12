#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric.api import env, put, run

env.hosts = ["34.74.141.15", "34.73.24.78"]


def do_deploy(archive_path):
    """distributes an archive to your web servers

    Arguments:
        archive_path (str): path of the archive
    Returns:
        (Bool) Returns False if the file at the path archive_path doesn’t exist
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

    steps = {
        "0": "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
        format(file, fname),
        "1": "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
        format(file, fname),
        "2": "rm /tmp/{}".format(file),
        "3": "mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(fname, fname),
        "4": "rm -rf /data/web_static/releases/{}/web_static".
        format(fname),
        "5": "rm -rf /data/web_static/current",
        "6": "ln -s /data/web_static/releases/{}/ /data/web_static/current".
        format(fname)
    }
    for i in steps.values():
        if run(i).failed is True:
            return False
    return True
