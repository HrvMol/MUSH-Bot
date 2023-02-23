import aiofiles
import discord


class Help(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.bot.help = ''

    @discord.Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded")
        async with aiofiles.open("help.md", mode = "r") as file:
            self.bot.explanation = await file.read()

    @discord.slash_command(description="Help command for the bot")
    async def help(self, ctx):
        await ctx.respond(self.bot.help)


def setup(bot):
    bot.add_cog(Help(bot))
