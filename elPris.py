#imports
from asyncio.tasks import wait
from requests_html import AsyncHTMLSession
from datetime import datetime
import random
import asyncio
import discord
from discord.ext import commands

async def dm(string):
    channel = await Client.fetch_channel("CHANNEL-ID")
    await channel.send(string)

async def HoursLookUp():
    now = datetime.now()
    print('!Hourly request. ' + now.strftime("%H:%M") + ': Checking...')
    asession = AsyncHTMLSession()
    r = await asession.get('https://elen.nu/dagens-spotpris/se4-malmo/')
    await r.html.arender()
    right = r.html.find('.text-right')
    left = r.html.find('.text-left')
    rightOffset = 2
    message = '`'
    for i in range(1,24):
        splitted = left[i].full_text.split()
        price = right[i + rightOffset].full_text
        if float(price.split()[0].replace(',','.')) < 100:
            price = price + ' 🔥🔥🔥'
        else:
            price = price + ' 💸'
        message = message + '\n' + splitted[1] + ' '  + price
        pass
    message = message + '`'
    await dm(message)
    pass

class Scraper:
    async def scrapeWorker(self):
        while True:
            ###
            self.now = datetime.now()
            print(self.now.strftime("%H:%M") + ': Checking...')

            ###
            r = await self.asession.get(self.url)
            await r.html.arender()
            result = r.html.find('.info-box-number')
            await self.CompileData(result)

            rand = 15*60 - 5*60*random.random()
            await asyncio.sleep(60 + rand)

    async def CompileData(self, result):
        if result[1].full_text != self.lastString:
            self.lastString = result[1].full_text
            pris = result[1].full_text + ' öre/kWh'
            if float(result[1].full_text) < 100:
                pris = pris + ' 🔥🔥🔥'
            else:
                pris = pris + ' 💸' 
            await dm(pris)

    def __init__(self):
        self.linkURL = ''
        self.lastString = ''
        self.lastName = ['','','']
        self.asession = AsyncHTMLSession()
        self.url = "https://elbruk.se/timpriser-se4-malmo"
        
        loop = asyncio.get_event_loop()
        try:
            print('Starting loop')
            asyncio.ensure_future(self.scrapeWorker())
        except KeyboardInterrupt:
            pass
        
if __name__ == '__main__':
    Client = discord.Client()
    
    @Client.event
    async def on_ready():
        print('We have logged in as')
        Scraper()

    @Client.event
    async def on_message(message):
        if message.author == Client.user:
            return

        if message.content.startswith('!hours'):
            await HoursLookUp()
            pass

    Client.run('BOT-KEY')
