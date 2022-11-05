import discord
from discord import Option


class Moderation(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.Cog.listener()
    async def on_ready(self):
        print("Moderation Cog Loaded")

    @discord.slash_command(description="remove a certain number of messages")
    # @discord.has_permissions(manage_messages = True)
    async def purge(self, ctx, messages: Option(int, description="How may messages do you want to purge?",
                                                requires=True)):
        i = await ctx.channel.purge(limit = messages)
        await ctx.respond(f'I have purged {len(i)} messages')


def setup(client):
    client.add_cog(Moderation(client))
