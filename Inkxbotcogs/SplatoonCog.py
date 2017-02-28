from discord.ext import commands
from .utils import config, checks, maps
import asyncio, aiohttp
from urllib.parse import quote as urlquote
import random
from collections import namedtuple
import discord




class Splatoon:
    """ Splatoon related commands. """

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('splatoon.json', loop=bot.loop)
        self.map_data = []
        self.map_updater = bot.loop.create_task(self.update_maps())

    def __unload(self):
        self.map_updater.cancel()

    async def splatnet_cookie(self):
        username = self.config.get('username')
        password = self.config.get('password')
        self.cookie = await maps.get_new_splatnet_cookie(username, password)

    async def update_maps(self):
        try:
            await self.splatnet_cookie()
            while not self.bot.is_closed:
                await self.update_schedule()
                await asyncio.sleep(120) # task runs every 2 minutes
        except asyncio.CancelledError:
            pass

    async def update_schedule(self):
        try:
            schedule = await maps.get_splatnet_schedule(self.cookie)
        except:
            # if we get an exception, keep the old data
            # make sure to remove the old data that already ended
            self.map_data = [data for data in self.map_data if not data.is_over]
        else:
            self.map_data = []
            for entry in schedule:
                if entry.is_over:
                    continue
                self.map_data.append(entry)

    def get_map_message(self, index):
        try:
            return str(self.map_data[index])
        except IndexError:
            return 'No map data found. Try again later.'

    @commands.event()
    async def loop_schedulecommand(self, ctx):


    @commands.command(hidden=True)
    async def refreshmaps(self, ctx):
        """Force refresh the maps in the rotation."""
        await self.update_schedule()
        await ctx.send('refreshed')

    @commands.command(aliases=['rotation'])
    async def maps(self, ctx):
        """Shows the current maps in the Splatoon schedule."""
        mps_embed = discord.Embed(title='SPLATOON SCHEDULE', description="{}".format(self.get_map_message(0)), color=0xFF8C00)
        await ctx.send(embed=mps_embed)

    @commands.command(hidden=True)
    async def nextmaps(self, ctx):
        """Shows the next maps in the Splatoon schedule."""
        await ctx.send(self.get_map_message(1))

    @commands.command(hidden=True)
    async def lastmaps(self, ctx):
        """Shows the last maps in the Splatoon schedule."""
        await ctx.send(self.get_map_message(2))

    @commands.command(aliases=['s'])
    async def schedule(self, ctx):
        """Shows the current Splatoon schedule."""
        sched_embed = discord.Embed(title='SPLATOON SCHEDULE', description="{}".format('\n'.join(map(str, self.map_data))), color=0xFF8C00)
        if self.map_data:
            await ctx.send(embed=sched_embed)
        else:
            await ctx.send('No map data found. Try again later.')

    @commands.command()
    async def woomy(self, ctx):
        '''Spams "Woomy!"'''
        await ctx.send('Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy! Woomy!')

def setup(bot):
    bot.add_cog(Splatoon(bot))
