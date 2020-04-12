#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import lcd, cd, local, env, run

env.hosts = ["34.74.141.15", "34.73.24.78"]


def do_clean(number=0):
    """Clean old archives.

    Arguments:
        number (int): The number of archives to keep.
    Returns:
        None
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    for _ in range(number):
        archives.pop()
    with lcd("versions"):
        for i in archives:
            local("rm ./{}".format(i))

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        for _ in range(number):
            archives.pop()
        for i in archives:
            local("rm ./{}".format(i))
