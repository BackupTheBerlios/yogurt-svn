#
# Yogurt/Configuration.py
#  - Interface to abstract Configuration.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['GlobalConf', 'Configuration']

class Configuration:

    # Detach from terminal and go background on POSIX systems. (True/False)
    daemonize = True

    # Show debug outputs into main logfile and also for stdout on forground.
    debug = False

GlobalConf = Configuration()
