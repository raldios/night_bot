# RolesCog.py

# imports
import discord
from discord.ext import commands


class RolesCog(commands.Cog):

    def __init__(self, night_bot, channel_id):
        self.night_bot = night_bot
        self._roles_channel_id = channel_id

    def set_roles_channel(self, channel_id: int):
        self._roles_channel_id = channel_id

    def validate_role(self, role_name):
        role = self.night_bot.get_role_from_name(role_name)
        valid = True if role is not None and role in self.night_bot.get_all_roles() else False
        return valid

    def init_roles_channel(self):
        channel = self.night_bot.get_channel(id=self._roles_channel_id)
        channel = self.night_bot.get_channel(name='roles')
