# FactsCog.py

# imports
import logging
import json
import discord
from discord.ext import commands
from pathlib import Path
from random import randrange
from datetime import datetime
from asyncio import sleep

WAIT_COOLDOWN = 60


class FactsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fact_ready = True

    async def get_facts(self, fact_group_str: str):
        channel = self.bot.get_channel_from_name(fact_group_str)
        return await channel.history(limit=123).flatten()

    async def get_random_fact(self, fact_group_str: str):
        messages = await self.get_facts(fact_group_str)
        rand_index = randrange(0, len(messages) - 1)
        return messages[rand_index].content

    @commands.command(name='getfact')
    async def getfact(self, ctx: discord.ext.commands.Context, *args):
        if len(args) < 1:
            await ctx.send('Please provide a fact type. :)')
        elif not self.fact_ready:
            await ctx.send('Please wait before trying again. :)')
        else:
            await ctx.send(await self.get_random_fact(args[0]))
            self.fact_ready = False
            await sleep(WAIT_COOLDOWN)
            self.fact_ready = True

    @commands.command(name='addfact')
    async def addfact(self, ctx: discord.ext.commands.Context, *args):
        fact_role = self.bot.get_role_from_name('fact adder')
        if len(args) < 2:
            await ctx.send('Please provide a fact.')
        if fact_role not in ctx.author.roles:
            await ctx.send('You are not allowed to do this. :)')

        channel = self.bot.get_channel_from_name(args[0])
        if channel is None: return
        await channel.send(args[1])
