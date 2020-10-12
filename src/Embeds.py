# Embed.py

import discord
from pathlib import Path

images = Path.cwd() / 'images'

wins_embed = discord.Embed(color=0x31eb31)
wins_embed.set_thumbnail(url='https://i.imgur.com/48c8ONd.png')
wins_embed.add_field(name='SUCCESS STORIES',
                     value="It's not easy to be queer in the world, but focusing on the bad can "
                           "harm your general mood. Small wins and big wins should be celebrated.",
                     inline=False)
wins_embed.add_field(name="Share Yours!",
                     value="List three wins from today, or yesterday if the day is just getting started. "
                           "Big or small, anything is good to celebrate.",
                     inline=False)

embeds = dict()
embeds['wins'] = wins_embed
