import discord


class Help(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        print("Help Cog Loaded")

    @discord.slash_command(description="Help command for the bot")
    # @discord.has_permissions(manage_messages = True)
    async def help(self, ctx):
        await ctx.respond(self.bot.help)


def setup(bot):
    bot.add_cog(Help(bot))
