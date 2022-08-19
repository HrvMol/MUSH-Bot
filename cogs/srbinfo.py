import discord
from discord.ext import commands
import aiofiles
from datetime import datetime, timezone


class Levelsys(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.bot.explaination = ''

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Info Cog Loaded")

        try:
            async with aiofiles.open("explain.txt", mode="r") as file:
                self.bot.explaination = await file.read()
        except: pass

    @commands.command(name='srb')
    async def srb(self, ctx, arg):
        closest = ''
        if arg == 'info':
            await ctx.send(self.bot.explaination)
            await ctx.message.delete()
        else:
            ctx.send('incorrect argument')


def setup(client):
    client.add_cog(Levelsys(client))