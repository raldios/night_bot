# RolesCog.py

# imports
import discord
from discord.ext import commands
from discord.utils import get
import logging

number_emoji_uni = [b'1\\u20e3', b'2\\u20e3', b'3\\u20e3', b'4\\u20e3',
                    b'5\\u20e3', b'6\\u20e3', b'7\\u20e3', b'8\\u20e3', b'9\\u20e3']

number_emoji_txt = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3',
                    '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3']


class RolesCog(commands.Cog):

    def __init__(self, night_bot, channel_id=None):
        self.bot = night_bot
        self.roles_channel_id = channel_id
        self.roles_dict = dict()

    def validate_role(self, role_name):
        role = self.bot.get_role_from_name(role_name)
        valid = True if role is not None and role in self.bot.get_all_roles() else False
        return valid

    @commands.command(name='init;roles')
    async def init_roles_channel(self, ctx):
        self.roles_dict = dict()
        messages = await self.bot.get_all_messages(self.roles_channel_id)

        for message in messages:
            lines = message.content.split('\n')
            emoji_index = 0
            for line in lines:
                if line[:2] == '**': continue
                line = line[4:]

                role = self.bot.get_role_from_name(line)
                if role:
                    logging.info(str(role) + ' found')
                    await message.add_reaction(number_emoji_txt[emoji_index])
                    emoji_index += 1
                else:
                    await self.bot.log.warning(f'role `{line}` '
                                                     f'not found during roles initialization <@82331305387241472>')
