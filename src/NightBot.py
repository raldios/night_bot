# Bot.py
import logging
import discord
from discord.ext import commands
from emoji import emojize

from cogs.ItemsCog import ItemsCog
from cogs.RolesCog import RolesCog, number_emoji_uni
from MyLogger import MyLogger


class NightBot(commands.Bot):

    def __init__(self, token, guild_name, init_channel_id, fact_cooldown, add_cooldown, log_filename):
        self.log = MyLogger(log_filename)
        intents = discord.Intents.default()
        intents.members = True
        commands.Bot.__init__(self, ';', guild_subscriptions=True, intents=intents)

        # attributes
        self.token = token
        self.guild_name = guild_name
        self.init_channel_id = int(init_channel_id)
        self.log_channel_id = None
        self.aliases = dict()

        # cogs
        self.facts_cog = ItemsCog(self, fact_cooldown, add_cooldown)
        self.roles_cog = RolesCog(self)

        # add cogs
        self.add_cog(self.facts_cog)
        self.add_cog(self.roles_cog)

        # flags
        self.skip_reaction_remove = False

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        logging.info('Connected Servers:')
        for guild in self.guilds: logging.info(guild)

        init_pairs = await self.get_bot_init_pairs()
        log_channel = self.get_channel(int(init_pairs['log']))
        roles_channel = self.get_channel(int(init_pairs['roles']))
        alias_channel = self.get_channel(int(init_pairs['alias']))

        logging.info(f'{log_channel.id} : {log_channel.name}')
        logging.info(f'{roles_channel.id} : {roles_channel.name}')
        logging.info(f'{alias_channel.id} : {alias_channel.name}')

        self.log_channel_id = int(init_pairs['log'])
        self.roles_cog.roles_channel_id = int(init_pairs['roles'])

        for message in await self.get_all_messages(int(init_pairs['alias'])):
            self.aliases[message.content.split()[0]] = message.content.split()[1]

    async def on_raw_reaction_add(self, payload):
        if not payload.channel_id == self.roles_cog.roles_channel_id: return
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.get_guild_from_name().get_member(payload.user_id)
        added_emoji_uni = payload.emoji.name.encode('unicode-escape')

        if added_emoji_uni not in number_emoji_uni:
            await message.remove_reaction(payload.emoji, member)
            self.skip_reaction_remove = True
            return

        lines = message.content.split('\n')[1:]
        index = number_emoji_uni.index(added_emoji_uni)
        role = self.get_role_from_name(lines[index][4:])

        await member.add_roles(role)
        await self.log.info(f'role {role.name} added to {member.nick}')

    async def on_raw_reaction_remove(self, payload):
        if self.skip_reaction_remove:
            self.skip_reaction_remove = False
            return

        if not payload.channel_id == self.roles_cog.roles_channel_id: return
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.get_guild_from_name().get_member(payload.user_id)
        added_emoji_uni = payload.emoji.name.encode('unicode-escape')

        lines = message.content.split('\n')[1:]
        index = number_emoji_uni.index(added_emoji_uni)
        role = self.get_role_from_name(lines[index][4:])

        if not role: return
        await member.remove_roles(role)
        await self.log.info(f'role {role} removed from {member.nick}')

    async def get_emoji_from_name(self, name: str, custom=True):
        if custom: emoji = discord.utils.get(self.emojis, name=name)

    async def get_emoji_code_from_name(self, name: str):
        return emojize(':one:', use_aliases=True).encode('unicode-escape')

    async def get_bot_init_pairs(self):
        init_pairs = dict()
        log = 'init pairs read\n'
        for message in await self.get_all_messages(self.init_channel_id):
            pair = message.content.split()
            log += f'`{message.content}`\n'
            init_pairs[pair[0]] = pair[1]

        return init_pairs

    async def get_all_messages(self, name_int):
        if type(name_int) == str: channel = self.get_channel_from_name(name_int)
        elif type(name_int) == int: channel = self.get_channel(name_int)
        else: return []

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

    def get_channel_from_name(self, name):
        guild: discord.Guild = self.get_guild_from_name()

        if name is not None:
            channel = discord.utils.get(guild.text_channels, name=name)
            return channel

    def get_log_channel(self):
        return self.get_channel(self.init_channel_id)

    def get_category_from_name(self, category_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.categories, name=category_name)

    def get_text_channels_from_category_name(self, category_name):
        category: discord.CategoryChannel = self.get_category_from_name(category_name)
        return category.text_channels
