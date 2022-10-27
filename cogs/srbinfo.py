import logging
from pydoc import describe
import discord
from discord.ext import commands
from discord.commands import slash_command
import aiofiles
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/srbinfo.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('INFO')

class SrbInfo(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.explanation = ''
        # GMT
        # self.bot.eu_srb_start = datetime.strptime("14:00:00", "%H:%M:%S")
        # self.bot.eu_srb_end = datetime.strptime("22:00:00", "%H:%M:%S")
        # self.bot.us_srb_start = datetime.strptime("01:00:00", "%H:%M:%S")
        # self.bot.us_stb_end = datetime.strptime("07:00:00", "%H:%M:%S")

        # BST
        self.bot.eu_srb_start = datetime.strptime("15:00:00", "%H:%M:%S")
        self.bot.eu_srb_end = datetime.strptime("23:00:00", "%H:%M:%S")
        self.bot.us_srb_start = datetime.strptime("02:00:00", "%H:%M:%S")
        self.bot.us_srb_end = datetime.strptime("08:00:00", "%H:%M:%S")

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Info Cog Loaded")

        try:
            async with aiofiles.open("explain.md", mode="r") as file:
                self.bot.explanation = await file.read()
        except: pass

    @slash_command(description="Information on SRB")
    async def srbinfo(self, ctx):
        await ctx.respond(self.bot.explanation)
        
    @slash_command(description="The time until the next SRBs")
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
            timeToUSEnd = (self.bot.us_srb_end - format_current)

            timeToEU = datetime.strftime(convert_to_format(timeToEU), "%H:%M:%S")
            timeToEUEnd = datetime.strftime(convert_to_format(timeToEUEnd), "%H:%M:%S")
            timeToUS = datetime.strftime(convert_to_format(timeToUS), "%H:%M:%S")
            timeToUSEnd = datetime.strftime(convert_to_format(timeToUSEnd), "%H:%M:%S")


            if timeToEU > timeToEUEnd and int(timeToEU[:2]) > 12:
                await ctx.respond(f'EU SRB window is currently open, closes in `{timeToEUEnd}` from now\n'
                                  f'Next US window opens in `{timeToUS}` from now')
            elif timeToUS > timeToUSEnd and int(timeToUS[:2]) > 12:
                await ctx.respond(f'US SRB window is currently open, closes in `{timeToUSEnd}` from now\n'
                                  f'Next EU window opens in `{timeToEU}` from now')
            else:
                await ctx.respond(f'Next EU window opens in `{timeToEU}` from now\n'
                                  f'Next US window opens in `{timeToUS}` from now')

        except Exception as error:
            logger.exception(error)



def setup(client):
    client.add_cog(SrbInfo(client))
