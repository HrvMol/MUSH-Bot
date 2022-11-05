import discord
from discord import commands
from discord import Option

bot = discord.Bot(command_prefix='!')


class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.qualified_name or "No Category", description=cog.description,
                              color=discord.Color.blurple())

        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No Help Message "
                                                                                                "Found... ")

        await self.get_destination().send(embed=embed)


bot.help_command = MyHelp()
