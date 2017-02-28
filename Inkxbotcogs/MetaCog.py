from discord.ext import commands
from .utils import checks, formats
import discord
from collections import OrderedDict, deque, Counter
import os, datetime
import re, asyncio
import copy
import unicodedata
import inspect


class Meta:
    """Commands for utilities related to Discord or about myself."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def charinfo(self, *, characters: str):
        """Shows you information about a number of characters in emojis.
        Only up to 15 characters at a time.
        """

        if len(characters) > 15:
            await self.bot.say('Too many characters ({}/15)'.format(len(characters)))
            return

        fmt = '`\\U{0:>08}`: {1} - {2} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{0}>'

        def to_string(c):
            digit = format(ord(c), 'x')
            name = unicodedata.name(c, 'Name not found.')
            return fmt.format(digit, name, c)

        await self.bot.say('\n'.join(map(to_string, characters)))

    @commands.command()
    async def source(self, command : str = None):
        """Displays my full source code or for a specific command."""
        source_url = 'https://github.com/InkxtheSquid/Inkxbot'
        if command is None:
            await self.bot.say(source_url)
            return

        code_path = command.split('.')
        obj = self.bot
        for cmd in code_path:
            try:
                obj = obj.get_command(cmd)
                if obj is None:
                    await self.bot.say('Could not find the command ' + cmd)
                    return
            except AttributeError:
                await self.bot.say('{0.name} command has no subcommands'.format(obj))
                return
        # since we found the command we're looking for, presumably anyway, let's
        # try to access the code itself
        src = obj.callback.__code__
        lines, firstlineno = inspect.getsourcelines(src)
        if not obj.callback.__module__.startswith('discord'):
            # not a built-in command
            location = os.path.relpath(src.co_filename).replace('\\', '/')
        else:
            location = obj.callback.__module__.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'

        final_url = '<{}/blob/master/{}#L{}-L{}>'.format(source_url, location, firstlineno, firstlineno + len(lines) - 1)
        await self.bot.say(final_url)

    @commands.command(rest_is_raw=True, hidden=True)
    @checks.is_owner()
    async def echo(self, *, content):
        await self.bot.say(content)

def setup(bot):
    bot.add_cog(Meta(bot))