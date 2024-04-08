#!/usr/bin/python3
"""creates and distributes an archive to your web servers
    using the function deploy"""


from fabric.api import *
import os
from fabric.operations import local
from datetime import datetime
import fabric


env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['34.204.61.147', '18.208.119.206']


def do_pack():
    """generates a.tgz archive from the contents"""
    try:
        if not os.path.exists("versions"):
            os.makedirs("versions")
        t = datetime.utcnow()
        a = "web_static_{}{}{}{}{}{}.tgz".format(t.year, t.month, t.day,
                                                 t.hour, t.minute, t.second)
        local("tar -cvzf versions/{} web_static".format(a))
        return a
    except Exception as e:
        return None


def do_deploy(archive_path):
    """distribute an archive to web server"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        a = os.path.basename(archive_path)
        b = a[:-4]
        run("mkdir -p /data/web_static/releases/{}/".format(b))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
            a, b))
        run("rm /tmp/{}".format(a))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(b, b))
        run("rm -rf /data/web_static/releases/{}/web_static".format(b))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(b))
        run("mv /data/web_static/current/index.html \
            /data/web_static/current/my_index.html")
        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
