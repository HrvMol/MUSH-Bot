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

# GMT
# eu_srb_start = datetime.strptime("14:00:00", "%H:%M:%S")
# eu_srb_end = datetime.strptime("22:00:00", "%H:%M:%S")
# us_srb_start = datetime.strptime("01:00:00", "%H:%M:%S")
# us_srb_end = datetime.strptime("07:00:00", "%H:%M:%S")


# BST
self.bot.eu_srb_start = datetime.strptime("15:00:00", "%H:%M:%S")
self.bot.eu_srb_end = datetime.strptime("23:00:00", "%H:%M:%S")
self.bot.us_srb_start = datetime.strptime("02:00:00", "%H:%M:%S")
self.bot.us_srb_end = datetime.strptime("08:00:00", "%H:%M:%S")

class SrbInfo(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.explanation = ''

    @commands.Cog.listener()
    async def on_ready(self):
        print("SRB Info Cog Loaded")

        try:
            async with aiofiles.open("explain.md", mode="r") as file:
                self.bot.explanation = await file.read()
        except:
            pass

    @discord.slash_command(name = "srbinfo", description="Information on SRB")
    async def srbinfo(self, ctx):
        await ctx.respond(self.bot.explanation)

    @discord.slash_command(name = "srbwhen", description="The time until the next SRB")
    async def srbwhen(self, ctx):
        try:
            def convert_to_format(td):
                hours, remainder = divmod(td.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return datetime.strptime(f'{hours}:{minutes}:{seconds}', "%H:%M:%S")

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            format_current = datetime.strptime(current_time, "%H:%M:%S")

            time_to_eu = (eu_srb_start - format_current) + timedelta(days=1)
            time_to_eu_end = (eu_srb_end - format_current)
            time_to_us = (us_srb_start - format_current) + timedelta(days=1)
            time_to_us_end = (us_srb_end - format_current)

            time_to_eu = datetime.strftime(convert_to_format(time_to_eu), "%H:%M:%S")
            time_to_eu_end = datetime.strftime(convert_to_format(time_to_eu_end), "%H:%M:%S")
            time_to_us = datetime.strftime(convert_to_format(time_to_us), "%H:%M:%S")
            time_to_us_end = datetime.strftime(convert_to_format(time_to_us_end), "%H:%M:%S")

            if time_to_eu > time_to_eu_end and int(time_to_eu[:2]) > 12:
                await ctx.respond(f'EU SRB window is currently open, closes in `{time_to_eu_end}` from now\n'
                                  f'Next US window opens in `{time_to_us}` from now')
            elif time_to_us > time_to_us_end and int(time_to_us[:2]) > 12:
                await ctx.respond(f'US SRB window is currently open, closes in `{time_to_us_end}` from now\n'
                                  f'Next EU window opens in `{time_to_eu}` from now')
            else:
                await ctx.respond(f'Next EU window opens in `{time_to_eu}` from now\n'
                                  f'Next US window opens in `{time_to_us}` from now')

        except Exception as error:
            logger.exception(error)


def setup(client):
    client.add_cog(SrbInfo(client))
