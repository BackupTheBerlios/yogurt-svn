#
# Yogurt/Commands/dependency.py
#  - checks python version and modules dependency.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['check']

import sys

def check():
    # Requires Python 2.3 or later
    if sys.hexversion < 0x2030000:
        return 'Python version 2.3 or later is required.'

    # Requires ZODB 3
    try:
        import ZODB
        if ZODB.__version__ < '3':
            return 'ZODB version must be higher than 3 at least.'
    except ImportError:
        return 'Yogurt needs ZODB package.'
