#
# Yogurt/IRC/IRCEvent.py
#  - Event meta class for IRC protocol.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['IRCEvent']

# XXX: make this inherit common event class
class IRCEvent:

    def __init__(self, conn, source, target, event, args):
        self.conn      = conn
        self.source    = source
        self.target    = target
        self.eventtype = event
        self.args      = args

    def __getattr__(self, key):
        return getattr(self.conn, key)
