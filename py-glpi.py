#!/usr/bin/env python
#coding:utf-8
import glpi_api
import json
import discord
from datetime import datetime, timedelta
from pprint import pprint
import logging
import configparser
import telepot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHAT_ID_TELEGRAM = os.getenv('IDCHAT_TELEGRAM')
CHANEL_DISCORD = os.getenv('CHANEL_DISCORD')
conf = configparser.ConfigParser()
conf.sections()
conf.read("config.ini")
listMensagens = []


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for chamado in listMensagens:
            channel = client.get_channel(CHANEL_DISCORD)
            await channel.send(chamado)

    async def on_message(self, message):
        if message.author == client.user:
            return
        channel = client.get_channel(CHANEL_DISCORD)
        await channel.send('👀')
        print(f'Message from {message.author}: {message.content}')


try:
    glpi_url = conf.get("glpi", "url")
    glpi_apptoken = conf.get("glpi","apptoken")
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


criteria = [ {
      "link":"AND",
      "field":"12",
      "searchtype":"equals",
      "value":"notold"
    },
    {
      "link":"AND",
      "field":"5",
      "searchtype":"contains",
      "value":"diogo da silva lima"
    }]

force_display=[1,2,5,19]  

chamadosAtualizacao = []

try:
    with glpi_api.connect(glpi_url, glpi_apptoken, glpi_token, False) as glpi:
        chamados = glpi.search('Ticket', criteria=criteria,forcedisplay=force_display)
        pprint(chamados)
        print(type(chamados))
        d = datetime.today() - timedelta(hours=0, minutes=30)
        print(d)
        atualizacoes = filter(lambda c: datetime.strptime(c['19'], '%Y-%m-%d %H:%M:%S') > d, chamados)
        chamadosAtualizacao = list(atualizacoes)

except glpi_api.GLPIError as err:
    print('error '+str(err))


intents = discord.Intents.default()
intents.message_content = True

#glpi = GLPI(glpi_url, glpi_apptoken, glpi_token)
bot = telepot.Bot(telegram_token)
bot.getMe()
response = bot.getUpdates()

for chamado in chamadosAtualizacao:
    messageTelegram = ".\n\nATENÇÃO🚨\n\nvocê tem um chamado que foi atualizado nos últimos 30 minutos\nchamado: {numChamado}\nacesse em: https://glpi.tce.rn.gov.br/front/ticket.form.php?id={numChamado}\n{tituloChamado}".format(numChamado=chamado['2'],tituloChamado=chamado['1'])
    listMensagens.append(messageTelegram)
    print(messageTelegram)
    bot.sendMessage(CHAT_ID_TELEGRAM, messageTelegram)


client = MyClient(intents=intents)
client.run(TOKEN)