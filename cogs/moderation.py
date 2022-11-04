from discord import Option
from discord.ext import commands
from discord.commands import slash_command


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation Cog Loaded")

    @slash_command(description="remove a certain number of messages")
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, messages: Option(int, description="How may messages do you want to purge?", requires=True)):
        i = await ctx.channel.purge(limit = messages)
        await ctx.respond(f'I have purged {len(i)} messages')

def setup(client):
    client.add_cog(Moderation(client))
