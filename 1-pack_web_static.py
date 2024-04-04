#!/usr/bin/python3
"""Fabric script that generates a .tgz archive"""

import fabric
import os
from fabric.operations import local
from datetime import datetime

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
