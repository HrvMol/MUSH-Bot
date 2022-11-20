import random
import discord


class EasterEggs(discord.Cog):  # Creates a class for the cog that inherits from commands.Cog
	# this class is used to create a cog, which is a module that can be added to the bot

	def __init__(self, bot):  # this is a special method that is called when the cog is loaded
		self.bot = bot

	@discord.Cog.listener()  # Adds an event listener to the cog
	async def on_ready(self):  # Called when the bot is ready
		print("Easter Egg Cog Loaded")

	@discord.Cog.listener()  # Adds an event listener to the cog
	async def on_message(self, ctx):
		print()
		if ctx.author != self.bot.user:
			if ctx.author.id == "407903863778312196":
				await ctx.channel.send("Not Tornado")
			if random.randint(0, 2500) == 1:
				await ctx.channel.send("fuck you")

	@discord.slash_command(name = "best")  # Creates a prefixed command
	async def best(self, ctx):
		image = "https://tinyurl.com/5yrzz5x6"
		await ctx.channel.send("Back Boris \n" + image)
		await ctx.message.delete()

	@discord.slash_command(name = "nephew")  # Creates a prefixed command
	async def nephew(self, ctx):
		image = "https://tinyurl.com/bdfmkupv"
		await ctx.channel.send("Head of the dinosaurs" + image)
		await ctx.message.delete()

	@discord.slash_command(name = "potatoes")  # Creates a prefixed command
	async def potatoes(self, ctx):
		image = "https://tenor.com/view/boom-bomb-car-bomb-explosion-detonate-gif-15743196"
		await ctx.channel.send("POV: you voted Tories" + image)
		await ctx.message.delete()

	@discord.slash_command(name = "salty")  # Creates a prefixed command
	async def salty(self, ctx):
		image = "https://tinyurl.com/2m3reh38"
		await ctx.channel.send("2 world wars, 1 world cup and 1 women's Euros" + image)
		await ctx.message.delete()

	@discord.slash_command(name = "russianbias")  # Creates a prefixed command
	async def russianbias(self, ctx):
		image = "https://tinyurl.com/4e2x43nd"
		await ctx.channel.send(image)
		await ctx.message.delete()

	@discord.slash_command(name = "scottsman")  # Creates a prefixed command
	async def scotsman(self, ctx):
		await ctx.channel.send(
			"https://cdn.discordapp.com/attachments/987513534227316789/1003431507597205584/received_272561204831416.jpeg")
		await ctx.message.delete()

	@discord.slash_command(name = "posh")  # Creates a prefixed command
	async def posh(self, ctx):
		await ctx.channel.send(
			"https://cdn.discordapp.com/attachments/987513534227316789/1005955570991370380/unknown.png")
		await ctx.message.delete()


def setup(bot):  # This is called by Pycord to set up the cog
	bot.add_cog(EasterEggs(bot))  # Adds the cog to the bot
