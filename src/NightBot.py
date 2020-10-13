# Bot.py
import logging
import discord
from discord.ext import commands

from cogs.FactsCog import FactsCog
from cogs.RolesCog import RolesCog

INIT_CHANNEL_NAME = 'init'


class NightBot(commands.Bot):

    def __init__(self, token, guild_name):
        commands.Bot.__init__(self, ';')

        # attributes
        self.token = token
        self.guild_name = guild_name
        self.log_channel_id = None

        # cogs
        self.facts_cog = FactsCog(self)
        self.roles_cog = RolesCog(self, None)

        # init cogs
        self.add_cog(self.facts_cog)
        self.add_cog(self.roles_cog)

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        logging.info('Connected Servers:')
        for guild in self.guilds:
            logging.info(guild)

        init_pairs = await self.get_bot_init_pairs()
        self.log_channel_id = init_pairs['log']
        self.roles_cog.set_roles_channel(init_pairs['roles'])

        self.roles_cog.init_roles_channel()

    async def get_bot_init_pairs(self):
        init_pairs = dict()
        log = 'pairs read\n'
        for message in await self.get_all_messages(INIT_CHANNEL_NAME):
            pair = message.content.split()
            log += f'`{message.content}`\n'
            init_pairs[pair[0]] = pair[1]

        log_channel: discord.TextChannel = self.get_channel(name='log')
        await log_channel.send(log)

        return init_pairs

    async def get_all_messages(self, fact_category: str):
        channel = self.get_channel(name=fact_category)
        return await channel.history(limit=500).flatten()

    def get_guild_from_name(self, guild_name=None):
        if guild_name is None: guild_name = self.guild_name
        return discord.utils.get(self.guilds, name=guild_name)

    def get_all_roles(self):
        guild: discord.Guild = self.get_guild_from_name()
        return guild.roles

    def get_role_from_name(self, roll_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.roles, name=roll_name)

    def get_channel(self, name=None, id=None):
        guild: discord.Guild = self.get_guild_from_name()

        if name is not None:
            channel = discord.utils.get(guild.text_channels, name=name)
            print(name, channel)
            return channel
        elif id is not None:
            channel = discord.utils.get(guild.text_channels, id=id)
            print(id, channel)
            return channel

    def get_category_from_name(self, category_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.categories, name=category_name)

    def get_text_channels_from_category_name(self, category_name):
        category: discord.CategoryChannel = self.get_category_from_name(category_name)
        return category.text_channels


