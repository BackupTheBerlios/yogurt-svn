#
# Yogurt/IRC/MessageTypes.py
#  - Message type/value constants for IRC protocol.
#
# This file is part of Yogurt.
#
# $Id$
#

__all__ = ['NUMERIC_MSGS', 'GENERATED_MSGS', 'PROTOCOL_MSGS', 'ALL_MSGS']

NUMERIC_MSGS = {
   '001': 'welcome',
   '002': 'yourhost',
   '003': 'created',
   '004': 'myinfo',
   '005': 'map', # Undernet Extension, Kajetan@Hinner.com, 17/11/98
   '006': 'mapmore', # Undernet Extension, Kajetan@Hinner.com, 17/11/98
   '007': 'mapend', # Undernet Extension, Kajetan@Hinner.com, 17/11/98
   '008': 'snomask', # Undernet Extension, Kajetan@Hinner.com, 17/11/98
   '009': 'statmemtot', # Undernet Extension, Kajetan@Hinner.com, 17/11/98
   '010': 'statmem', # Undernet Extension, Kajetan@Hinner.com, 17/11/98

   '200': 'tracelink',
   '201': 'traceconnecting',
   '202': 'tracehandshake',
   '203': 'traceunknown',
   '204': 'traceoperator',
   '205': 'traceuser',
   '206': 'traceserver',
   '208': 'tracenewtype',
   '209': 'traceclass',
   '211': 'statslinkinfo',
   '212': 'statscommands',
   '213': 'statscline',
   '214': 'statsnline',
   '215': 'statsiline',
   '216': 'statskline',
   '217': 'statsqline',
   '218': 'statsyline',
   '219': 'endofstats',
   '221': 'umodeis',
   '231': 'serviceinfo',
   '232': 'endofservices',
   '233': 'service',
   '234': 'servlist',
   '235': 'servlistend',
   '241': 'statslline',
   '242': 'statsuptime',
   '243': 'statsoline',
   '244': 'statshline',
   '245': 'statssline', # Reserved, Kajetan@Hinner.com, 17/10/98
   '246': 'statstline', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '247': 'statsgline', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '248': 'statsuline', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '249': 'statsdebug', # Unspecific Extension, Kajetan@Hinner.com, 17/10/98
   '250': 'statsconn', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   #'250': 'luserconns', # 1998-03-15 -- tkil
   '251': 'luserclient',
   '252': 'luserop',
   '253': 'luserunknown',
   '254': 'luserchannels',
   '255': 'luserme',
   '256': 'adminme',
   '257': 'adminloc1',
   '258': 'adminloc2',
   '259': 'adminemail',
   '261': 'tracelog',
   '262': 'endoftrace', # 1997-11-24 -- archon
   '265': 'n_local', # 1997-10-16 -- tkil
   '266': 'n_global', # 1997-10-16 -- tkil
   '271': 'silelist', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '272': 'endofsilelist', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '275': 'statsdline', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '280': 'glist', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '281': 'endofglist', # Undernet Extension, Kajetan@Hinner.com, 17/10/98

   '300': 'none',
   '301': 'away',
   '302': 'userhost',
   '303': 'ison',
   '305': 'unaway',
   '306': 'nowaway',
   '307': 'userip', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '310': 'whoishelp', # (July01-01)Austnet Extension,
                       # found by Andypoo <andypoo@secret.com.au>
   '311': 'whoisuser',
   '312': 'whoisserver',
   '313': 'whoisoperator',
   '314': 'whowasuser',
   '315': 'endofwho',
   '316': 'whoischanop',
   '317': 'whoisidle',
   '318': 'endofwhois',
   '319': 'whoischannels',
   '320': 'whoisvworld', # (July01-01)Austnet Extension,
                         # found by Andypoo <andypoo@secret.com.au>
   '321': 'liststart',
   '322': 'list',
   '323': 'listend',
   '324': 'channelmodeis',
   '329': 'channelcreate', # 1997-11-24 -- archon
   '331': 'notopic',
   '332': 'topic',
   '333': 'topicinfo', # 1997-11-24 -- archon
   '334': 'listusage', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '341': 'inviting',
   '342': 'summoning',
   '351': 'version',
   '352': 'whoreply',
   '353': 'namreply',
   '354': 'whospcrpl', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '361': 'killdone',
   '362': 'closing',
   '363': 'closeend',
   '364': 'links',
   '365': 'endoflinks',
   '366': 'endofnames',
   '367': 'banlist',
   '368': 'endofbanlist',
   '369': 'endofwhowas',
   '371': 'info',
   '372': 'motd',
   '373': 'infostart',
   '374': 'endofinfo',
   '375': 'motdstart',
   '376': 'endofmotd',
   '377': 'motd2', # 1997-10-16 -- tkil
   '378': 'austmotd', # (July01-01)Austnet Extension,
                      # found by Andypoo <andypoo@secret.com.au>
   '381': 'youreoper',
   '382': 'rehashing',
   '384': 'myportis',
   '385': 'notoperanymore', # Unspecific Extension, Kajetan@Hinner.com,
                            # 17/10/98
   '391': 'time',
   '392': 'usersstart',
   '393': 'users',
   '394': 'endofusers',
   '395': 'nousers',

   '401': 'nosuchnick',
   '402': 'nosuchserver',
   '403': 'nosuchchannel',
   '404': 'cannotsendtochan',
   '405': 'toomanychannels',
   '406': 'wasnosuchnick',
   '407': 'toomanytargets',
   '409': 'noorigin',
   '411': 'norecipient',
   '412': 'notexttosend',
   '413': 'notoplevel',
   '414': 'wildtoplevel',
   '416': 'querytoolong', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '421': 'unknowncommand',
   '422': 'nomotd',
   '423': 'noadmininfo',
   '424': 'fileerror',
   '431': 'nonicknamegiven',
   '432': 'erroneusnickname', # This iz how its speld in thee RFC.
   '433': 'nicknameinuse',
   '436': 'nickcollision',
   '437': 'bannickchange', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '438': 'nicktoofast', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '439': 'targettoofast', # Undernet Extension, Kajetan@Hinner.com, 17/10/98

   '441': 'usernotinchannel',
   '442': 'notonchannel',
   '443': 'useronchannel',
   '444': 'nologin',
   '445': 'summondisabled',
   '446': 'usersdisabled',
   '451': 'notregistered',
   '461': 'needmoreparams',
   '462': 'alreadyregistered',
   '463': 'nopermforhost',
   '464': 'passwdmismatch',
   '465': 'yourebannedcreep',
   '466': 'youwillbebanned',
   '467': 'keyset',
   '468': 'invalidusername', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '471': 'channelisfull',
   '472': 'unknownmode',
   '473': 'inviteonlychan',
   '474': 'bannedfromchan',
   '475': 'badchannelkey',
   '476': 'badchanmask',
   '478': 'banlistfull', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '481': 'noprivileges',
   '482': 'chanoprivsneeded',
   '483': 'cantkillserver',
   '484': 'ischanservice', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '491': 'nooperhost',
   '492': 'noservicehost',

   '501': 'umodeunknownflag',
   '502': 'usersdontmatch',

   '511': 'silelistfull', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '513': 'nosuchgline', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
   '513': 'badping', # Undernet Extension, Kajetan@Hinner.com, 17/10/98
}

GENERATED_MSGS = [
    'disconnect',
    'ctcp',
    'ctcpreply',
    'minutes',
    'seconds',
    'login',
    'logout',
]

PROTOCOL_MSGS = [
    'error',
    'join',
    'kick',
    'mode',
    'nick',
    'part',
    'ping',
    'privmsg',
    'privnotice',
    'pubmsg',
    'pubnotice',
    'servermsg',
    'servernotice',
    'quit'
]

ALL_MSGS = GENERATED_MSGS + PROTOCOL_MSGS + NUMERIC_MSGS.values()
