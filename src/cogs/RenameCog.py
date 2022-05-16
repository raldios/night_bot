# RenameCog.py

# imports
import discord
from discord.ext import commands


class RenameCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rename_disabled = False

    @commands.command(name='toggle_rename')
    async def toggle_rename(self, ctx: discord.ext.commands.Context, *args):
        self.rename_disabled = not self.rename_disabled

        if self.rename_disabled: status = "disabled"
        else: status = "enabled"

        await ctx.send(f'rename command set to {status}.')

    @commands.command(name='rename')
    async def rename(self, ctx: discord.ext.commands.Context, *args):
        if await self.disabled_check(ctx): return

        elif await self.length_check(ctx, args, 1):
            name = ' '.join(args)
        else: return

        try:
            channel: discord.VoiceChannel = ctx.message.author.voice.channel
        except AttributeError:
            await self.bot.log.info(
                f'{ctx.message.author} tried to rename a channel while not connected to a voice channel.')
            await ctx.send('Please connect to the voice channel you want to rename.')
            return

        await channel.edit(name=name)
        await self.bot.log.info(f'{ctx.message.author} renamed voice channel {channel.name} to {name}.')

    async def disabled_check(self, ctx):
        if self.rename_disabled:
            await ctx.send('Command `rename` is currently disabled.')
            return True
        else:
            return False

    async def length_check(self, ctx, items_list, min_length):
        if len(items_list) < min_length:
            await ctx.send('Please give a name to rename the channel.')
            await self.bot.log.info(
                f'{ctx.message.author} tried to rename a channel without giving the new name.')
            return False
        else:
            return True



