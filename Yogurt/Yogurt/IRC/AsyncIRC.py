#
# Yogurt/IRC/AsyncIRC.py
#  - Asynchronous IRC Channel.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['IRCChannel']

import socket, re
import asyncore, asynchat
from cStringIO import StringIO
from Yogurt.IRC.MessageTypes import ALL_MSGS, NUMERIC_MSGS
from Yogurt.IRC.Protocol import *
from Yogurt.IRC.IRCEvent import IRCEvent

class IRCChannel(asynchat.async_chat):
    
    def __init__(self, addr, nick, password='', username=None, fullname=None):
        self.real_servername = ''
        self.real_nickname = ''
        self.addr = addr
        self.nickname = nick
        self.password = password
        self.username = username or self.nickname
        self.fullname = fullname or self.username
        self.fqdn = socket.getfqdn()
        self.handlers = {}
        self.reset_handlers()
        self.eventstack = []

        asynchat.async_chat.__init__(self)
        # XXX: check configuration if target server is in IPv6 network.
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(addr)

        self.buffer = StringIO()
        self.set_terminator('\r\n')

    def reset_handlers(self):
        self.handlers.clear()
        self.handlers[None] = [] # global
        for event in ALL_MSGS:
            self.handlers[event] = []

    def add_handler(self, event, handler):
        if event is None or event in ALL_MSGS:
            self.handlers[event].append(handler)
        else:
            raise ValueError, "%s: undefined irc event" % event

    def remove_handler(self, event, handler):
        if self.handlers.has_key(event):
            self.handlers[event].remove(handler) # thru ValueError
        else:
            raise ValueError, "%s: undefined irc event" % event

    def handle_connect(self):
        if self.password:
            self.pass_(self.password)
        self.nick(self.nickname)
        self.user(self.username, self.fqdn, self.addr[0], self.fullname)
        # XXX: addr must inet

    def handle_close(self):
        self.handle_event(IRCEvent(self, '', None, "disconnect",
                ['Connection reset by the peer']))
        self.close()

    def collect_incoming_data(self, data):
        self.buffer.write(data)

    def found_terminator(self):
        data = self.buffer.getvalue()
        self.buffer.seek(0,0)
        self.buffer.truncate()
        m = rfc1459parse.match(data)
        if not m:
            return

        if m.group('prefix'):
            prefix = m.group('prefix')
            if not self.real_servername:
                self.real_servername = prefix
        else:
            prefix = ''

        if m.group('command'):
            command = m.group("command").lower()
        else:
            return

        if m.group('argument'):
            a = m.group('argument').split(' :', 1)
            args = a[0].split()
            if len(a) == 2:
                args.append(a[1])

        if command in ('privmsg', 'notice'):
            target, messages = args[0], ctcp_dequote(args[1])

            if command == 'privmsg':
                command = is_channel(target) and 'pubmsg' or 'privmsg'
            else:
                command = is_channel(target) and 'pubnotice' or 'privnotice'

            for msg in messages:
                if isinstance(msg, tuple): # CTCP
                    event = command.endswith('msg') and 'ctcp' or 'ctcpreply'
                    self.handle_event(IRCEvent(self, prefix, target, event, list(msg)))
                else:
                    event = command
                    self.handle_event(IRCEvent(self, prefix, target, event, [msg]))
        elif command == 'quit':
            self.handle_event(IRCEvent(self, prefix, None, 'quit', args))
        elif command == 'ping':
            self.pong(args[0])
        elif command.isdigit():
            event = NUMERIC_MSGS.get(command)
            if event:
                self.handle_event(IRCEvent(self, prefix, args[0], event, args[1:]))
        else:
            self.handle_event(
                IRCEvent(self, prefix, args[0], command, args[1:]) )

        while self.eventstack:
            self.handle_event(self.eventstack.pop(0))

    def push_event(self, ev):
        self.eventstack.append(ev)

    def handle_event(self, event):
        for hdl in self.handlers[None] + self.handlers[event.eventtype]:
            hdl(event)

    def sendline(self, s):
        s = str(s).replace('\n', '').replace('\r', '')
        if len(s) < MESSAGE_MAXLEN:
            self.push(s + '\r\n')
        else:
            self.push(s[:MESSAGE_MAXLEN] + '\r\n')

    # == Command Set ==

    def action(self, target, action):
        self.ctcp("ACTION", target, action)

    def admin(self, server=""):
        self.sendline(' '.join(["ADMIN", server]).strip())

    def ctcp(self, ctcptype, target, parameter=""):
        ctcptype = ctcptype.upper()
        self.privmsg(target, "\x01%s%s\x01" % (ctcptype, parameter and (" " + parameter) or ""))

    def ctcp_reply(self, target, parameter):
        self.notice(target, "\x01%s\x01" % parameter)

    def disconnect(self, message=""):
        if not self.connected:
            return

        self.handle_event(IRCEvent(self, self.real_server, None, "disconnect", [message]))
        self.close()

    def globops(self, text):
        self.sendline("GLOBOPS :" + text)

    def info(self, server=""):
        self.sendline(' '.join(["INFO", server]).strip())

    def invite(self, nick, channel):
        self.sendline(' '.join(["INVITE", nick, channel]).strip())

    def ison(self, nicks):
        self.sendline("ISON " + ','.join(nicks))

    def join(self, channel, key=""):
        self.sendline("JOIN %s%s" % (channel, (key and (" " + key))))

    def kick(self, channel, nick, comment=""):
        self.sendline("KICK %s %s%s" % (channel, nick, (comment and (" :" + comment))))

    def links(self, remote_server="", server_mask=""):
        command = "LINKS"
        if remote_server:
            command = command + " " + remote_server
        if server_mask:
            command = command + " " + server_mask
        self.sendline(command)

    def list(self, channels=None, server=""):
        command = "LIST"
        if channels:
            command = command + " " + ','.join(channels)
        if server:
            command = command + " " + server
        self.sendline(command)

    def lusers(self, server=""):
        self.sendline("LUSERS" + (server and (" " + server)))

    def mode(self, target, command):
        self.sendline("MODE %s %s" % (target, command))

    def motd(self, server=""):
        self.sendline("MOTD" + (server and (" " + server)))

    def names(self, channels=None):
        self.sendline("NAMES" + (channels and (" " + ','.join(channels)) or ""))

    def nick(self, newnick):
        self.sendline("NICK " + newnick)

    def notice(self, target, text):
        self.sendline("NOTICE %s :%s" % (target, text))

    def oper(self, nick, password):
        self.sendline("OPER %s %s" % (nick, password))

    def part(self, channels):
        if isinstance(channels, str):
            self.sendline("PART " + channels)
        else:
            self.sendline("PART " + ','.join(channels))

    def pass_(self, password):
        self.sendline("PASS " + password)

    def ping(self, target, target2=""):
        self.sendline("PING %s%s" % (target, target2 and (" " + target2)))

    def pong(self, target, target2=""):
        self.sendline("PONG %s%s" % (target, target2 and (" " + target2)))

    def privmsg(self, target, text):
        if isinstance(target, str):
            self.sendline("PRIVMSG %s :%s" % (target, text))
        elif isinstance(target, list) or isinstance(target, tuple):
            self.sendlist("PRIVMSG %s :%s" % (','.join(target), text))

    def quit(self, message=""):
        self.sendline("QUIT" + (message and (" :" + message)))

    def sconnect(self, target, port="", server=""):
        self.sendline("CONNECT %s%s%s" % (target,
                                          port and (" " + port),
                                          server and (" " + server)))

    def squit(self, server, comment=""):
        self.sendline("SQUIT %s%s" % (server, comment and (" :" + comment)))

    def stats(self, statstype, server=""):
        self.sendline("STATS %s%s" % (statstype, server and (" " + server)))

    def time(self, server=""):
        self.sendline("TIME" + (server and (" " + server)))

    def topic(self, channel, new_topic=None):
        if new_topic == None:
            self.sendline("TOPIC " + channel)
        else:
            self.sendline("TOPIC %s :%s" % (channel, new_topic))

    def trace(self, target=""):
        self.sendline("TRACE" + (target and (" " + target)))

    def user(self, username, localhost, server, ircname):
        self.sendline("USER %s %s %s :%s" % (username, localhost, server, ircname))

    def userhost(self, nicks):
        self.sendline("USERHOST " + ','.join(nicks))

    def users(self, server=""):
        self.sendline("USERS" + (server and (" " + server)))

    def version(self, server=""):
        self.sendline("VERSION" + (server and (" " + server)))

    def wallops(self, text):
        self.sendline("WALLOPS :" + text)

    def who(self, target="", op=""):
        self.sendline("WHO%s%s" % (target and (" " + target), op and (" o")))

    def whois(self, targets):
        self.sendline("WHOIS " + ','.join(targets))

    def whowas(self, nick, max=None, server=""):
        self.sendline("WHOWAS %s%s%s" % (nick,
                                         max and (" " + max),
                                         server and (" " + server)))


if __name__ == '__main__':
    def join(ev):
        ev.join('#cube')

    def echomsg(ev):
        ev.privmsg(ev.target, ev.args[0])

    def testlog(ev):
        print "<IRCEvent source='%s' target='%s' event='%s' args=%s>" % (
                ev.source, ev.target, ev.eventtype, repr(ev.args) )
        
    i = IRC(('nttmcl.hanirc.org', 6667), 'neocube', username='username', fullname='fullname')
    i.add_handler(None, testlog)
    i.add_handler('welcome', join)
    i.add_handler('pubmsg', echomsg)
    asyncore.loop()
