# ItemsCog.py

# imports
import discord
from discord.ext import commands
from random import randrange
from asyncio import sleep
import logging


class ItemsCog(commands.Cog):

    def __init__(self, bot, fact_cooldown, add_cooldown):
        self.bot = bot
        self.fact_cooldown = int(fact_cooldown)
        self.add_cooldown = int(add_cooldown)
        self.get_ready = True
        self.add_ready = True

    def get_item_channels(self):
        return self.bot.get_text_channels_from_category_name('item channels')

    async def get_random_item(self, fact_category: str):
        facts = await self.bot.get_all_messages(fact_category)
        rand_index = randrange(0, len(facts))
        return facts[rand_index].content

    def validate_item_category(self, fact_category):
        if fact_category is None: return False
        bot_channels = self.get_item_channels()
        valid = False if len([x for x in bot_channels if x.name == fact_category]) < 1 else True
        return valid

    @commands.command(name='get')
    async def get(self, ctx: discord.ext.commands.Context, item_category=None, *args):
        if item_category in self.bot.aliases.keys():
            logging.info(f'{item_category} aliased to {self.bot.aliases[item_category]}')
            item_category = self.bot.aliases[item_category]

        if not self.get_ready:
            await ctx.send('Please wait before trying again. :)')
        elif not self.validate_item_category(item_category):
            await ctx.send('Please provide a valid item type. :)')
        else:
            await ctx.send(await self.get_random_item(item_category))
            self.get_ready = False
            await sleep(self.fact_cooldown)
            self.get_ready = True

    @commands.command(name='count')
    async def count(self, ctx: discord.ext.commands.Context, item_category=None, *args):
        if not self.validate_item_category(item_category):
            await ctx.send('Please provide a valid item type. :)')
        else:
            items = await self.bot.get_all_messages(item_category)
            await ctx.send(f'There are {len(items)} {item_category} facts!')

    @commands.command(name='add')
    async def add(self, ctx: discord.ext.commands.Context, category=None, *item_words):
        valid_categories = [category.name for category in self.bot.get_text_channels_from_category_name('item channels')]
        valid_categories.remove('katie')

        if category is None or category not in valid_categories:
            await ctx.send('Please provide a valid category. :)')

        item_str = " ".join(item_words)
        item_channel: discord.TextChannel = self.bot.get_channel_from_name(category)

        properly_formatted = (item_str[:3] == '```' and item_str[-3:] == '```')

        if category == 'quote' and not properly_formatted:
            await ctx.send('All quotes must start and end with three backticks. (```)  :)')
        else:
            await item_channel.send(item_str)
