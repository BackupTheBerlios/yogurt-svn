#
# Yogurt/Commands/yogurt.py
#  - yogurt bringing up control script.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['main']

import os, sys
from Yogurt.Utilities import sysutils
from Yogurt.Configuration import GlobalConf

def mkparser():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-f', '--foreground', action='store_false',
                      dest='daemonize', default=GlobalConf.daemonize,
                      help="don't go background")
    parser.add_option('-d', '--debug', action='store_true',
                      dest='debug', default=GlobalConf.debug,
                      help='show debug prints')
    return parser

def setcmdlineoptions(options):
    GlobalConf.daemonize = options.daemonize
    GlobalConf.debug = options.debug

def showbanner():
    print """\
\x1b[1;37mY\x1b[33mo\x1b[37mg\x1b[36mu\x1b[37mrt\x1b[0m -\
 a well-being IRC bot. ;-)  [http://yogurt.python.or.kr]
"""

def run():
    pass

def main():
    showbanner()
    sysutils.setstatus('initializing')
    options, args = mkparser().parse_args()
    if options.daemonize:
        sysutils.daemonize()

    setcmdlineoptions(options)
    try:
        run()
    except (KeyboardInterrupt, SystemExit):
        pass
    except:
        # XXX: print exception only if debug mode is on.
        import traceback
        traceback.print_exc()
