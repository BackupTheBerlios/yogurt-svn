#
# Yogurt/Logging.py
#  - Yogurt logging support.
#
# This file is part of Yogurt.
#
# $Id$
#

import logging
from urllib import quote

class Loggers:
    def __init__(self, logroot, minlevel):
        self.logroot = logroot
        self.loglevel = logging.getLevelName(minlevel)
        self.loggers = {}
        self.logstreams = []

    def __getitem__(self, key):
        qkey = quote(key)
        if self.loggers.has_key(qkey):
            return self.loggers[qkey]

        log  = logging.getLogger(qkey)
        hdlr = logging.handlers.RotatingFileHandler(
                    "%s/%s" % (self.logroot, qkey),
                    maxBytes=1048576, backupCount=5)
        fmt = logging.Formatter('%(asctime)s:%(levelname)-5s:%(message)s',
                                '%x %X')
        hdlr.setFormatter(fmt)
        log.addHandler(hdlr)

        for st in self.logstreams:
            hdlr = logging.StreamHandler(st)
            fmt = logging.Formatter(
                    '[%s] %%(levelname)-5s:%%(message)s' %
                        key.replace('%', '%%'), '%x %X')
            hdlr.setFormatter(fmt)
            log.addHandler(hdlr)

        log.setLevel(self.loglevel)
        self.loggers[qkey] = log
        return log

    def __delitem__(self, key):
        key = quote(key)
        if self.loggers.has_key(key):
            del self.loggers[key]

    def addstream(self, st):
        self.logstreams.append(st)

    def setlevel(self, lvl):
        self.loglevel = lvl
        logging.setLevel(lvl)
        for logger in self.loggers.itervalues():
            logger.setLevel(lvl)
