from discord.ext import commands
from .utils import config, checks#, hcards
import asyncio, aiohttp
from urllib.parse import quote as urlquote
from collections import namedtuple
import requests

class Hearthstone:
    def __init__(self, bot):
        self.bot = bot
        #self.loop = AbstractEventLoop.run_in_executor()

        """def get_cards(self):
        #You can change for fitting your language deDE, enUS, esES, esMX,
        #frFR, itIT, jaJP, koKR, plPL, ptBR, ruRU, thTH, zhCN, zhTW
        response = requests.get('https://api.hearthstonejson.com/v1/12574/enUS/cards.collectible.json')#, 'https://api.hearthstonejson.com/v1/13619/enUS/cards.collectible.json', 'https://api.hearthstonejson.com/v1/15181/enUS/cards.collectible.json', 'https://api.hearthstonejson.com/v1/15300/enUS/cards.collectible.json')#
        data = response.json()
        return data


        @commands.command()
        async def hearthcard(self, args):
        data = get_cards()
        cardname = data['"name": 'args]
        attack = data['"attack": ']
        if data["type": "MINION"] == True:
            await ctx.send('**{0}** \n' +
            """


    @commands.command(pass_context=True)
    async def hearthwiki(self, title, ctx):
        """Returns a hearthstone wiki page: ,hearthwiki 'card name'"""
        url = 'http://hearthstone.wikia.com/wiki/' + urlquote(title)
        typetochan = ctx.message.channel
        async with aiohttp.get(url) as resp:
            if resp.status == 404:
                await ctx.send('Could not find your page. Try a search:\n<{0.url}>'.format(resp))
            elif resp.status == 200:
                await ctx.send(resp.url)
            elif resp.status == 502:
                await ctx.send('Seems like the Hearthstone Wiki is taking too long to respond. Try again later.')
            else:
                await ctx.send('An error has occurred of status code {0.status} happened. Tell Inkx.'.format(resp))

def setup(bot):
    bot.add_cog(Hearthstone(bot))
