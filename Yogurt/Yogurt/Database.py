#
# Yogurt/Database.py
#  - Package initializer for Yogurt.Database.
#
# This file is part of Yogurt.
#
# $Id$
#

import os, os.path
from UserDict import UserDict
import Persistence, PersistentMapping
from ZODB import DB, FileStorage,  PersistentList

__all__ = ['Entry', 'ListEntry', 'DictEntry', 'Database', 'DatabaseManager']

class Entry(Persistence.Persistent):
    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

ListEntry = PersistentList.PersistentList
DictEntry = PersistentMapping.PersistentMapping

class Database(UserDict):
    def __init__(self, file):
        self.db = DB(FileStorage.FileStorage(file))
        self.connection = self.db.open()
        self.data = self.connection.root()

    def commit(self):
        get_transaction().commit()

class DatabaseManager:
    def __init__(self, dbroot='data'):
        self.dbroot = dbroot
        if not os.access(dbroot, os.W_OK):
            try:
                os.makedirs(os.path.join(dbroot, '/cube'))
            except:
                dmesg.exception("Can't make database directory or not writable")
                raise SystemExit
        self.databases = {}

    def __getitem__(self, (modname, dbname)):
        filename = os.path.join(self.dbroot, modname, dbname)+'.fs'
        if not self.databases.has_key(filename):
            try:
                dirname = os.path.join(self.dbroot, modname)
                if not os.access(dirname, os.F_OK):
                    os.makedirs(dirname)
                self.databases[filename] = Database(filename)
            except:
                dmesg.exception("Can't create database : %s", filename)
                return None
        return self.databases[filename]
