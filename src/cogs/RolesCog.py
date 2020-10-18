# RolesCog.py

# imports
import discord
from discord.ext import commands
from discord.utils import get
import logging


class RolesCog(commands.Cog):

    def __init__(self, night_bot, channel_id=None):
        self.night_bot = night_bot
        self.roles_channel_id = channel_id
        self.roles_dict = dict()

    def validate_role(self, role_name):
        role = self.night_bot.get_role_from_name(role_name)
        valid = True if role is not None and role in self.night_bot.get_all_roles() else False
        return valid

    @commands.command(name='init;roles')
    async def init_roles_channel(self, ctx):
        self.roles_dict = dict()
        messages = await self.night_bot.get_all_messages(self.roles_channel_id)

        for message in messages:
            if message.content[:2] == '**': continue

            role = self.night_bot.get_role_from_name(message.content)
            if role:
                trans_this = discord.utils.get(self.night_bot.emojis, name='transThis')
                await message.add_reaction(trans_this)
            else:
                log_channel = self.night_bot.get_channel(self.night_bot.log_channel_id)

                await log_channel.send(f'role `{message.content}` '
                                       f'not found during roles initialization <@82331305387241472>')
                logging.warning(f'role {message.content} not found during roles initialization')

                x = discord.utils.get(self.night_bot.emojis, name='rooScream')
                logging.info(x)
                await message.add_reaction(x)

