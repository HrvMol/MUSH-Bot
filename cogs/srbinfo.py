import logging
import discord
from discord.ext import commands
import aiofiles
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/srbinfo.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('INFO')

class Levelsys(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.explaination = ''
        # GMT
        # self.bot.eu_srb_start = datetime.strptime("14:00:00", "%H:%M:%S")
        # self.bot.eu_srb_end = datetime.strptime("22:00:00", "%H:%M:%S")
        # self.bot.us_srb_start = datetime.strptime("01:00:00", "%H:%M:%S")
        # self.bot.us_stb_end = datetime.strptime("07:00:00", "%H:%M:%S")

        # BST
        self.bot.eu_srb_start = datetime.strptime("15:00:00", "%H:%M:%S")
        self.bot.eu_srb_end = datetime.strptime("23:00:00", "%H:%M:%S")
        self.bot.us_srb_start = datetime.strptime("02:00:00", "%H:%M:%S")
        self.bot.us_stb_end = datetime.strptime("08:00:00", "%H:%M:%S")

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Info Cog Loaded")

        try:
            async with aiofiles.open("explain.txt", mode="r") as file:
                self.bot.explaination = await file.read()
        except: pass

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        await ctx.send(f'Synced {len(fmt)} commands.')

    @commands.command(name='srbinfo', description="information on SRB")
    async def srbinfo(self, ctx):
        await ctx.send(self.bot.explaination)
        # await ctx.message.delete()
        
    @commands.command(name='srbwhen')
    async def srbwhen(self, ctx):
        try:
            def convert_to_format(td):
                hours, remainder = divmod(td.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return datetime.strptime(f'{hours}:{minutes}:{seconds}', "%H:%M:%S")

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            format_current = datetime.strptime(current_time, "%H:%M:%S")

            timeToEU = (self.bot.eu_srb_start - format_current) + timedelta(days=1)
            timeToEUEnd = (self.bot.eu_srb_end - format_current)
            timeToUS = (self.bot.us_srb_start - format_current) + timedelta(days=1)
            timeToUSEnd = (self.bot.eu_srb_end - format_current)

            timeToEU = datetime.strftime(convert_to_format(timeToEU), "%H:%M:%S")
            timeToEUEnd = datetime.strftime(convert_to_format(timeToEUEnd), "%H:%M:%S")
            timeToUS = datetime.strftime(convert_to_format(timeToUS), "%H:%M:%S")
            timeToUSEnd = datetime.strftime(convert_to_format(timeToUSEnd), "%H:%M:%S")

            if timeToEU > timeToEUEnd and int(timeToEU[:2]) > 12:
                await ctx.send(f'EU SRB window is currently open \nNext US window opens in: `{timeToUS}`')
            elif timeToUS > timeToUSEnd and int(timeToUS[:2]) > 12:
                await ctx.send(f'US SRB window is currently open \nNext EU window opens in: `{timeToEU}`')
            else:
                await ctx.send(f'Next EU window opens in: `{timeToEU}`\nNext US window opens in: `{timeToUS}`')

            await ctx.message.delete()
        except Exception as error:
            logger.exception(error)



def setup(client):
    client.add_cog(Levelsys(client))