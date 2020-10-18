# Bot.py
import logging
import discord
from discord.ext import commands

from cogs.FactsCog import FactsCog
from cogs.RolesCog import RolesCog

INIT_CHANNEL_ID = 765277853151395910


class NightBot(commands.Bot):

    def __init__(self, token, guild_name):
        commands.Bot.__init__(self, ';')

        # attributes
        self.token = token
        self.guild_name = guild_name
        self.log_channel_id = None

        # cogs
        self.facts_cog = FactsCog(self)
        self.roles_cog = RolesCog(self)

        # add cogs
        self.add_cog(self.facts_cog)
        self.add_cog(self.roles_cog)

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        logging.info('Connected Servers:')
        for guild in self.guilds: logging.info(guild)

        init_pairs = await self.get_bot_init_pairs()
        log_channel = self.get_channel(int(init_pairs['log']))
        roles_channel = self.get_channel(int(init_pairs['roles']))

        logging.info(f'{log_channel.id} : {log_channel.name}')
        logging.info(f'{roles_channel.id} : {roles_channel.name}')

        self.log_channel_id = int(init_pairs['log'])
        self.roles_cog.roles_channel_id = int(init_pairs['roles'])

    async def on_raw_reaction_add(self, payload):
        if self.user.id == payload.user_id: return
        elif not payload.channel_id == self.roles_cog.roles_channel_id: return
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.get_guild_from_name().get_member(payload.user_id)
        trans_this = discord.utils.get(self.emojis, name='transThis')
        added_emoji = discord.utils.get(self.emojis, name=payload.emoji.name)

        if not added_emoji == trans_this:
            await message.remove_reaction(added_emoji, member)
            return

        role = self.get_role_from_name(message.content)
        await member.add_roles(role)
        logging.info(f'role {message.content} added to {member.nick}')

    async def on_raw_reaction_remove(self, payload):
        if not payload.channel_id == self.roles_cog.roles_channel_id: return
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.get_guild_from_name().get_member(payload.user_id)

        role = self.get_role_from_name(message.content)
        await member.add_roles(role)
        logging.info(f'role {message.content} added to {member.nick}')

    async def get_bot_init_pairs(self):
        init_pairs = dict()
        log = 'init pairs read\n'
        for message in await self.get_all_messages(INIT_CHANNEL_ID):
            pair = message.content.split()
            log += f'`{message.content}`\n'
            init_pairs[pair[0]] = pair[1]

        log_channel: discord.TextChannel = self.get_channel_from_name(name='log')
        return init_pairs

    async def get_all_messages(self, channel_id: int):
        channel = self.get_channel(channel_id)
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

    def get_category_from_name(self, category_name):
        guild: discord.Guild = self.get_guild_from_name()
        return discord.utils.get(guild.categories, name=category_name)

    def get_text_channels_from_category_name(self, category_name):
        category: discord.CategoryChannel = self.get_category_from_name(category_name)
        return category.text_channels
