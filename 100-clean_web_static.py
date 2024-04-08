#!/usr/bin/python3
""" Fabric script that deletes out of date archive"""


import os
from fabric.api import *


env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'
env.hosts = ['34.204.61.147', '18.208.119.206']


def do_clean(number=0):
    """deletes out of date archives"""
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1
    local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
          .format(number))
    run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {{}} \
          rm /data/web_static/releases/{{}}".format(number))
