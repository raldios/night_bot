# Bot.py
import logging
import json
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
import discord
from discord.ext import commands, tasks
from pathlib import Path
import asyncio

from cogs.DailiesManagementCog import DailiesManagementCog
from cogs.FactsCog import FactsCog
from Embeds import embeds


class Bot(commands.Bot):

    def __init__(self, token, guild_name, timezone, json_folder):
        commands.Bot.__init__(self, ';')

        self.token = token
        self.guild_name = guild_name
        self.timezone = ZoneInfo(timezone)
        self.json_path = Path.cwd().parent / json_folder
        if not self.json_path.exists():
            self.json_path.mkdir()
        self.dailies_path = str(self.json_path / 'dailies.json')
        self.dailies_cog = DailiesManagementCog(self)
        self.facts_cog = FactsCog(self)

        self.add_cog(self.dailies_cog)
        self.add_cog(self.facts_cog)

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        logging.info('Connected Servers:')
        for guild in self.guilds:
            logging.info(guild)

        self.dailies_loop.start()

    def get_guild(self):
        pass
        # todo make guild retrieval function

    def get_role(self, roll_name):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        return discord.utils.get(guild.roles, name=roll_name)

    def get_channel(self, channel_name):
        guild: discord.Guild = discord.utils.get(self.guilds, name=self.guild_name)
        return discord.utils.get(guild.channels, name=channel_name)

    def get_daily(self, daily_str=None):
        with open(self.dailies_path, 'r') as in_file:
            if daily_str is not None:
                return json.load(in_file)[daily_str]
            else:
                return json.load(in_file)

    async def import_facts(self):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        katie_channel = discord.utils.get(guild.text_channels, id=764972790775939082)
        with open('katie facts.txt', 'r', encoding="utf8") as file:
            for line in file.readlines():
                await katie_channel.send(line)

    @tasks.loop(hours=24)
    async def dailies_loop(self):
        logging.info('dailies_loop triggered')
        await self.dailies_cog.trigger_event(event='wins')

    @dailies_loop.before_loop
    async def before_dailies_loop(self):
        logging.info('before dailies_loop triggered')
        hour = self.get_daily('wins')['hour']
        if hour > 23: hour -= 24
        minute = 0

        now = datetime.now()
        future = datetime(now.year, now.month, now.day, hour, minute)

        if now.hour >= hour and now.minute > minute:
            future += timedelta(days=1)

        await asyncio.sleep((future - now).seconds)


