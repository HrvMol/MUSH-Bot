from xml.dom import expatbuilder
import discord
from discord.ext import commands
import aiofiles



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

    @commands.command(name='explain')
    async def explain(self, ctx):
        await ctx.send(self.bot.explaination)
        await ctx.message.delete()

def setup(client):
    client.add_cog(Levelsys(client))