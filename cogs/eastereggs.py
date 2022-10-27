import discord
from discord.ext import commands
import random


class EasterEggs(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Easter Egg Cog Loaded")

	@commands.Cog.listener()
	async def on_message(self, ctx):
		print()
		if ctx.author != self.bot.user:
			if ctx.author.id == "407903863778312196":
				await ctx.channel.send("Not Tornado")
			if random.randint(0, 2500) == 1:
				await ctx.channel.send("fuck you")

	@commands.command(name = "best")
	async def best(self, ctx):
		image = "https://tinyurl.com/5yrzz5x6"
		await ctx.channel.send("Back Boris" + image)
		await ctx.message.delete()

	@commands.command(name = "nephew")
	async def nephew(self, ctx):
		image = "https://tinyurl.com/bdfmkupv"
		await ctx.channel.send("Head of the dinosaurs" + image)
		await ctx.message.delete()

	@commands.command(name = "potatoes")
	async def potatoes(self, ctx):
		image = "https://tenor.com/view/boom-bomb-car-bomb-explosion-detonate-gif-15743196"
		await ctx.channel.send("POV: you voted Tories" + image)
		await ctx.message.delete()


	@commands.command(name = "russianbias")
	async def russianbias(self, ctx):
		image = "https://tinyurl.com/4e2x43nd"
		await ctx.channel.send(image)
		await ctx.message.delete()

    @commands.command(name="salty")
    async def salty(self, ctx):
        image = "https://tinyurl.com/2m3reh38"
        await ctx.channel.send("2 world wars, 1 world cup and 1 women's Euros" + image)
        await ctx.message.delete()
	@commands.command(name = "scottsman")
	async def scotsman(self, ctx):
		await ctx.channel.send(
			"https://cdn.discordapp.com/attachments/987513534227316789/1003431507597205584/received_272561204831416.jpeg")
		await ctx.message.delete()

	@commands.command(name = "posh")
	async def posh(self, ctx):
		await ctx.channel.send(
			"https://cdn.discordapp.com/attachments/987513534227316789/1005955570991370380/unknown.png")
		await ctx.message.delete()


def setup(client):
	client.add_cog(EasterEggs(client))
