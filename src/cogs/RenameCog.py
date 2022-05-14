# RenameCog.py

# imports
import discord
from discord.ext import commands
from random import randrange
from asyncio import sleep
import logging


def concat_args(*args):
    text = str()
    for arg in args:
        text = text + arg

    return text


class RenameCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rename_disabled = False

    @commands.command(name='toggle_rename')
    async def toggle_rename(self, ctx: discord.ext.commands.Context, *args):
        self.rename_disabled = not self.rename_disabled

        if self.rename_disabled: status = "disabled"
        else: status = "enabled"

        await ctx.send(f'toggle_rename set to {status}.')

    @commands.command(name='rename')
    async def rename(self, ctx: discord.ext.commands.Context, name=None, *args):
        if self.rename_disabled:
            await ctx.send('Command `rename` is currently disabled.')

        if not name:
            await ctx.send('Please give a name to rename the channel.')
            return

        channel: discord.VoiceChannel = ctx.message.author.voice.voice_channel
        if not channel:
            await ctx.send('Please connect to the voice channel you want to rename.')
            return

        name = concat_args(args)
        channel.name = name
        await ctx.send(f'Channel renamed to `{name}`.')
