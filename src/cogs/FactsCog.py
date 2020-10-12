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

    def get_fact_channels(self):
        return self.bot.get_text_channels_from_category_name('bot channels')

    async def get_facts(self, fact_category: str):
        channel = self.bot.get_channel_from_name(fact_category)
        return await channel.history(limit=500).flatten()

    async def get_random_fact(self, fact_category: str):
        facts = await self.get_facts(fact_category)
        rand_index = randrange(0, len(facts) - 1)
        return facts[rand_index].content

    def validate_fact_category(self, fact_category):
        if fact_category is None: return False
        bot_channels = self.get_fact_channels()
        valid = False if len([x for x in bot_channels if x.name == fact_category]) < 1 else True
        return valid

    @commands.command(name='getfact')
    async def getfact(self, ctx: discord.ext.commands.Context, fact_category=None, *args):
        if not self.fact_ready:
            await ctx.send('Please wait before trying again. :)')
        elif not self.validate_fact_category(fact_category):
            await ctx.send('Please provide a valid fact type. :)')
        else:
            await ctx.send(await self.get_random_fact(fact_category))
            self.fact_ready = False
            await sleep(WAIT_COOLDOWN)
            self.fact_ready = True

    @commands.command(name='factcount')
    async def factcount(self, ctx: discord.ext.commands.Context, fact_category=None, *args):
        if not self.validate_fact_category(fact_category):
            await ctx.send('Please provide a valid fact type. :)')
        else:
            facts = await self.get_facts(fact_category)
            await ctx.send(f'There are {len(facts)} {fact_category} facts!')
