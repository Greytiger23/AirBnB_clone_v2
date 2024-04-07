#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy"""


from fabric.api import env, put, run
import os
from fabric.operations import local
from datetime import datetime


env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['34.204.61.147', '18.208.119.206']


def do_pack():
    """generates a.tgz archive from the contents"""
    local("mkdir -p versions")
    t = datetime.utcnow()
    a = "web_static_{}{}{}{}{}{}.tgz".format(t.year, t.month, t.day,
                                             t.hour, t.minute, t.second)
    b = local("tar -cvzf versions/{} web_static".format(a))
    if b.failed:
        return None
    else:
        return os.path.abspath("versions/{}".format(a))

def do_deploy(archive_path):
    """distribute an archive to web server"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        a = os.path.basename(archive_path)
        b = os.path.splitext(a)[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(b))
        run('tar -xzf /tmp{} -C /data/web_static/releases/{}/'.format(
            a, b))
        run('rm /tmp/{}'.format(a))
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(b, b))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(b))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(b))
        print("New version deploed!")
        return True
    except Exception as e:
        return False
