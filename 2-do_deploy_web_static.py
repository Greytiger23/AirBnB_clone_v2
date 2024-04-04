#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy"""

from fabric.api import env, put, run
import os


env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['xx-web-01', 'xx-web-02']


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
        run('mv /data/web_static/releases/{}/web_static/* /data
            /web_static/releases/{}/'.format(b, b))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(b))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(b))
        print("New version deploed!")
        return True
    except Exception as e:
        return False
