#
# Yogurt/I18N/DummyRegistry.py
#  - Dummy translation registry that does nothing.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['register', 'lookup']

def lookup(fmt):
    return fmt

def register():
    import __builtin__
    __builtin__._ = lookup
