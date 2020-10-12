# Bot.py
import logging
import json
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from pathlib import Path
import asyncio

from cogs.FactsCog import FactsCog


class Bot(commands.Bot):

    def __init__(self, token, guild_name, timezone, json_folder):
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

    async def import_facts(self, facts_filename):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        katie_channel = discord.utils.get(guild.text_channels, id=764972790775939082)

        with open(facts_filename, 'r', encoding="utf8") as file:
            for line in file.readlines():
                await katie_channel.send(line)


