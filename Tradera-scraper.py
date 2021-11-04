#imports
from asyncio.tasks import wait
from requests_html import AsyncHTMLSession
from datetime import datetime
import random
import asyncio
import discord
from discord.ext import commands

async def dm(string):
    user = await Client.fetch_user("CHANNEL-ID")
    await user.send(string)

class Scraper:
    async def scrapeWorker(self):
        while True:
            ###
            self.now = datetime.now()
            print(self.now.strftime("%H:%M") + ': Checking...')

            ###
            r = await self.asession.get(self.url)
            await r.html.arender()
            result = r.html.find('.item-card-container')
            await self.CompileData(result)

            rand = -30 + 60*random.random()
            await asyncio.sleep(60 + rand)

    async def CompileData(self, result):
        ind = -1
        var1 = result[0].links.pop()
        var2 = result[1].links.pop()
        var3 = result[2].links.pop()

        # checks for update
        if self.lastName[0] != var1:
            ind = 0
            pass
        elif self.lastName[1] != var2:
            ind = 1
            pass
        elif self.lastName[2] != var3:
            ind = 2
            pass
        else:
            return
        
        #update last 3 data points
        self.lastName[0] = var1
        self.lastName[1] = var2
        self.lastName[2] = var3
        
        
        ####
        linkURL = self.lastName[ind]
        self.linkURL = 'https://www.tradera.com' + linkURL
        
        #### price
        r = await self.asession.get(self.linkURL)
        await r.html.arender() 
        btns = r.html.find('.btn-success')
        index = 0

        if len(btns) == 2:
            index = 1
            
        s = r.html.find('.btn-success')[index]
        price = s.full_text.replace("\u2006", " ")

        #### name
        s = r.html.find('#view-item-main')[0]
        title = s.text
        
        print('\033[41m' + self.now.strftime("%H:%M") + ': ' + title + '.\nPris: ' + price + '\033[0m\n\033[41m'  + self.linkURL + '\033[0m')
        await dm(self.now.strftime("%H:%M") + ': ' + title + '.\nPris: '+ price + ' \n ' + self.linkURL)
        pass

    def __init__(self):
        self.linkURL = ''
        self.lastName = ['','','']
        self.asession = AsyncHTMLSession()
        self.url = "https://www.tradera.com/category/120303?itemType=FixedPrice&sortBy=AddedOn"
        
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

    Client.run('BOT-KEY')