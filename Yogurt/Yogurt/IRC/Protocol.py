#
# Yogurt/IRC/Protocol.py
#  - IRC Protocol library functions.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['MESSAGE_MAXLEN', 'rfc1459parse', 'is_channel', 'match_mask',
           'parse_nick_modes', 'parse_channel_modes', 'nm2n', 'nm2uh', 'nm2h',
           'nm2u', 'nm_to_n', 'nm_to_uh', 'nm_to_h', 'nm_to_u', 'ctcp_dequote',
           'IRCDict', 'IRCChannel']
import re
import string

_LOW_LEVEL_QUOTE  = '\x10'
_CTCP_LEVEL_QUOTE = '\x5c'
_CTCP_DELIMITER   = '\x01'
MESSAGE_MAXLEN = 400

rfc1459parse = re.compile('^(:(?P<prefix>[^ ]+) +)?(?P<command>[^ ]+)'
                          '( *(?P<argument> .+))?')
is_channel = lambda x: x and x[0] == '#'

_low_level_mapping = {
    '0': '\x00',
    'n': '\n',
    'r': '\r',
    _LOW_LEVEL_QUOTE: _LOW_LEVEL_QUOTE
}
_low_level_regexp = re.compile(_LOW_LEVEL_QUOTE + '(.)')

def ctcp_dequote(message):

    def _low_level_replace(match_obj):
        ch = match_obj.group(1)
        return _low_level_mapping.get(ch, ch)

    if _LOW_LEVEL_QUOTE in message:
        message = _low_level_regexp.sub(_low_level_replace, message)

    if _CTCP_DELIMITER not in message:
        return [message]
    else:
        chunks = message.split(_CTCP_DELIMITER)

        messages = []
        i = 0
        while i < len(chunks)-1:
            if len(chunks[i]) > 0:
                messages.append(chunks[i])

            if i < len(chunks)-2:
                messages.append(tuple(chunks[i+1].split(' ', 1)))

            i = i + 2

        if len(chunks) % 2 == 0:
            messages.append(_CTCP_DELIMITER + chunks[-1])

        return messages


from fnmatch import fnmatchcase
def match_mask(nick, mask):
    return fnmatchcase(irclower(mask), irclower(nick))

lowertable = string.maketrans('[]\\^'+string.uppercase,
                              '{}|~'+string.lowercase)
def irclower(s):
    return s.translate(lowertable)

def parse_nick_modes(mode_string):
    return _parse_modes(mode_string, "")

def parse_channel_modes(mode_string):
    return _parse_modes(mode_string, "bklvo")

def _parse_modes(mode_string, unary_modes=""):
    modes = []
    arg_count = 0

    sign = ""

    a = mode_string.split()
    if len(a) == 0:
        return []
    else:
        mode_part, args = a[0], a[1:]

    if mode_part[0] not in "+-":
        return []
    for ch in mode_part:
        if ch in "+-":
            sign = ch
        elif ch == " ":
            collecting_args = 1
        elif ch in unary_modes and arg_count < len(args):
            modes.append([sign, ch, args[arg_count]])
            arg_count = arg_count + 1
        else:
            modes.append([sign, ch, None])
    return modes

def nm_to_n(s):
    return s.split("!")[0]

def nm_to_uh(s):
    return s.split("!")[1]

def nm_to_h(s):
    return s.split("@")[1]

def nm_to_u(s):
    return s.split('!')[-1].split('@')[0]

nm2n, nm2uh, nm2h, nm2u = nm_to_n, nm_to_uh, nm_to_h, nm_to_u


class IRCDict(dict):
    def __init__(self):
        dict.__init__(self)
        self.canonkey = {}
    
    def __getitem__(self, key):
        return dict.__getitem__(self, self.canonkey[irclower(key)])

    def __setitem__(self, key, value):
        dict.__setitem__(self, self.canonkey.setdefault(irclower(key), key),
                         value)

    def __delitem__(self, key):
        ck = irclower(key)
        dict.__delitem__(self, self.canonkey[ck])
        del self.canonkey[ck]

    def clear(self):
        dict.clear(self)
        self.canonkey.clear()

    def has_key(self, key):
        return self.canonkey.has_key(irclower(key))

    def get(self, key, fail=None):
        ck = irclower(key)
        if self.canonkey.has_key(ck):
            return dict.__getitem__(self, self.canonkey[ck])
        else:
            return fail


class IRCChannel:

    def __init__(self):
        self.userdict = IRCDict()
        self.operdict = IRCDict()
        self.voiceddict = IRCDict()
        self.modes = {}

    def users(self):
        return self.userdict.keys()

    def opers(self):
        return self.operdict.keys()

    def voiced(self):
        return self.voiceddict.keys()

    def has_user(self, nick):
        return self.userdict.has_key(nick)

    def is_oper(self, nick):
        return self.operdict.has_key(nick)

    def is_voiced(self, nick):
        return self.voiceddict.has_key(nick)

    def add_user(self, nick):
        self.userdict[nick] = 1

    def remove_user(self, nick):
        for d in self.userdict, self.operdict, self.voiceddict:
            if d.has_key(nick):
                del d[nick]

    def change_nick(self, before, after):
        self.userdict[after] = 1
        del self.userdict[before]
        if self.operdict.has_key(before):
            self.operdict[after] = 1
            del self.operdict[before]
        if self.voiceddict.has_key(before):
            self.voiceddict[after] = 1
            del self.voiceddict[before]

    def set_mode(self, mode, value=None):
        if mode == "o":
            self.operdict[value] = 1
        elif mode == "v":
            self.voiceddict[value] = 1
        else:
            self.modes[mode] = value

    def clear_mode(self, mode, value=None):
        try:
            if mode == "o":
                del self.operdict[value]
            elif mode == "v":
                del self.voiceddict[value]
            else:
                del self.modes[mode]
        except KeyError:
            pass

    def has_mode(self, mode):
        return mode in self.modes

    def is_moderated(self):
        return self.has_mode("m")

    def is_secret(self):
        return self.has_mode("s")

    def is_protected(self):
        return self.has_mode("p")

    def has_topic_lock(self):
        return self.has_mode("t")

    def is_invite_only(self):
        return self.has_mode("i")

    def has_message_from_outside_protection(self):
        # Eh... What should it be called, really?
        return self.has_mode("n")

    def has_limit(self):
        return self.has_mode("l")

    def limit(self):
        if self.has_limit():
            return self.modes[l]
        else:
            return None

    def has_key(self):
        return self.has_mode("k")

    def key(self):
        if self.has_key():
            return self.modes["k"]
        else:
            return None
