#
# Yogurt/Utilities/sysutils.py
#  - Utilities collection that covers system stuff.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['daemonize', 'setstatus']

import os, sys

def daemonize_posix():
    os.setsid()
    if os.fork():
        os._exit(0)

    nullrfd = os.open('/dev/null', os.O_RDONLY)
    os.dup2(nullrfd, sys.stdin.fileno())
    os.close(nullrfd)

    nullwfd = os.open('/dev/null', os.O_RDWR)
    os.dup2(nullwfd, sys.stdout.fileno())
    os.dup2(nullwfd, sys.stderr.fileno())
    os.close(nullwfd)
    os.setsid()

def daemonize_noop():
    pass

if os.name == 'posix':
    daemonize = daemonize_posix
else:
    daemonize = daemonize_noop

try:
    from freebsd import setproctitle as _setproctitle
    from freebsd import setprogname as _setprogname
except ImportError:
    def _setproctitle(title): pass
    def _setprogname(name): pass

def setstatus(status):
    _setprogname('yogurt')
    _setproctitle(status)
