#!/usr/bin/env python
#coding:utf-8

import json
from glpi import GLPI
from glpi import GlpiProfile
from glpi import GlpiTicket, Ticket
from pprint import pprint
import logging
import ConfigParser
import telepot

# Читаем конфиг
conf = ConfigParser.RawConfigParser()
conf.read("config.ini")

# секция glpi, посвященная подключению к API
try:
    glpi_url = conf.get("glpi", "url")
    glpi_user = conf.get("glpi", "user")
    glpi_password = conf.get("glpi", "password")
    glpi_token = conf.get("glpi", "token")
except ConfigParser.NoSectionError:
    logging.error(u"Can't read glpi section in config.ini")
    raise SystemExit(1)

# секция telegram, посвященная подключению к telegram-api
try:
    telegram_token = conf.get("telegram", "token")
except ConfigParser.NoSectionError:
    logging.error(u"Can't read telegram section in config.ini")
    raise SystemExit(1)
glpi = GLPI(glpi_url, glpi_token, (glpi_user, glpi_password))
bot = telepot.Bot(telegram_token)

bot.getMe()
response = bot.getUpdates()
pprint(response)
#bot.sendMessage(180318137, "!Privet it is Python Bot :)")
#logging.warning(u'Test warning MESSAGE')

"""
print "Getting all Tickets: "
print json.dumps(glpi.get_all('ticket'),
                  indent=4,
                  separators=(',', ': '),
                  sort_keys=True)
"""