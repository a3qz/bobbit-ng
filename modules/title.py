# title.py

from modules.__common__ import strip_html

import re

import tornado.gen
import tornado.httpclient

# Metadata

NAME    = 'title'
ENABLE  = True
TYPE    = 'command'
PATTERN = '.*(?P<url>http[^\s]+$).*'
USAGE   = '''Usage: !g <query>
Looks up title of URL.
Example:
    > http://www.insidehighered.com/quicktakes/2019/06/24/uc-santa-cruz-removes-catholic-mission-bell
    Title: UC Santa Cruz Removes Catholic Mission Bell
'''

# Constants

WHITELIST = ('##bx612', '##grillers', '#nd-cse', '#uwec-cs')

# Command

@tornado.gen.coroutine
def command(bot, nick, message, channel, url=None):
    if channel is not None and channel not in WHITELIST:
        return

    client = tornado.httpclient.AsyncHTTPClient()
    result = yield tornado.gen.Task(client.fetch, url)

    try:
        body     = result.body.decode('utf-8').replace('\n', ' ')
        title    = re.findall(r'<title[^>]*>([^<]+)</title>', body)[0]
        title    = strip_html(title)
        response = bot.format_text('{color}{green}Title{color}: {bold}{title}{bold}', title=title)
    except (IndexError, ValueError) as e:
        return

    bot.send_response(response, nick, channel)

# Register

def register(bot):
    return (
        (PATTERN, command),
    )

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
