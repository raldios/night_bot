# DailiesCog.py

# imports
import logging
import json
import discord
from discord.ext import commands
from datetime import time
from pathlib import Path

from Embeds import embeds

raldios = 82331305387241472
ons = ['true', 'on', 'yes']
offs = ['false', 'off', 'no']


class DailiesManagementCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dailies = self.load_dailies()
        self.dump_dailies()

    @commands.command(name='daily')
    async def daily(self, context, *args):
        if context.message.author.id != raldios: return

        logging.info('daily command triggered')
        logging.info(f'args: {args}')

        if args[0] == 'set' and args[1] == 'help':
            await context.send('usage: `;daily set <event> <key> <value>`')
        elif args[0] == 'create' and args[1] == 'help':
            await context.send('usage: `;daily create <event>`')
        elif args[0] == 'delete' and args[1] == 'help':
            await context.send('usage: `;daily delete <event>`')
        elif args[0] == 'set' and len(args) == 4:
            event = args[1]
            key = args[2]
            value = args[3]
            await self.set_option(context, event, key, value)
        elif args[0] == 'create' and len(args) == 2:
            event = args[1]
            await self.create_event(context, event)
        elif args[0] == 'delete' and len(args) == 2:
            event = args[1]
            await self.delete_event(context, event)
        elif args[0] == 'trigger' and len(args) == 2:
            await self.trigger_event(context, args[1])

    def load_dailies(self):
        path: Path = self.bot.json_path / 'dailies.json'

        if not path.exists():
            path: Path = self.bot.json_path / 'dailies_default.json'
        else:
            path: Path = self.bot.json_path / 'dailies.json'

        with open(str(path), 'r') as in_file:
            return json.load(in_file)

    def dump_dailies(self):
        path = self.bot.json_path / 'dailies.json'
        with open(path, 'w') as out_file:
            json.dump(self.dailies, out_file, indent=4)

    def print_dailies(self, context=None):
        logging.info(json.dumps(self.dailies, indent=4))

    async def set_option(self, context, event, key, value):

        if key not in ['active', 'hour', 'channel_id']:
            await context.send('Please provide a valid key to set `active`, `hour`, `channel_id`')
            return
        elif key == 'active':
            value = bool(value.lower() != 'false')
        elif key in ['hour', 'channel_id']:
            value = int(value)

        if event in self.dailies.keys():
            if key in self.dailies[event].keys():
                self.dailies[event][key] = value

        self.dump_dailies()
        logging.info(f'`{event} : {key}` set to `{value}`')
        await context.send(f'`{event} : {key}` set to `{value}`')

    async def create_event(self, context, event):
        if event in self.dailies.keys():
            await context.send(f'`event : {event}` already exists')
            return

        self.dailies[event] = {
            "active": False,
            "hour": None,
            "channel_id": None,
            'last_date': None
        }
        self.dump_dailies()

        await context.send(f'`event : {event}` created')

    async def delete_event(self, context, event):
        if event not in self.dailies.keys():
            await context.send(f'`event : {event}` is not a created event')
            return

        del self.dailies[event]
        self.dump_dailies()

        await context.send(f'`event : {event}` deleted')

    async def trigger_event(self, context=None, event=None):
        if context is not None:
            if event not in embeds:
                await context.send(f'`{event}` does not have an associated embed')
                return

        event_dict = self.dailies[event]
        guild = discord.utils.get(self.bot.guilds, name=self.bot.guild_name)
        channel = discord.utils.get(guild.text_channels, id=event_dict['channel_id'])
        channel = discord.utils.get(guild.text_channels, id=699006303443615759)  # test channel

        await channel.send(None, embed=embeds[event])


