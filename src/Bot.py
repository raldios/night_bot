# Bot.py
import logging
import discord
from discord.ext import commands

from cogs.FactsCog import FactsCog


class Bot(commands.Bot):

    def __init__(self, token, guild_name):
        commands.Bot.__init__(self, ';')

        self.token = token
        self.guild_name = guild_name
        self.facts_cog = FactsCog(self)

        self.add_cog(self.facts_cog)

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        logging.info('Connected Servers:')
        for guild in self.guilds:
            logging.info(guild)

    def get_guild_from_name(self, guild_name=None):
        if guild_name is None: guild_name = self.guild_name
        return discord.utils.get(self.guilds, name=guild_name)

    def get_role_from_name(self, roll_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.roles, name=roll_name)

    def get_channel_from_name(self, channel_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.channels, name=channel_name)

    def get_category_from_name(self, category_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.categories, name=category_name)

    def get_text_channels_from_category_name(self, category_name):
        category: discord.CategoryChannel = self.get_category_from_name(category_name)
        return category.text_channels


