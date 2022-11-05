import discord
from discord.ext import commands
import json
import logging
from typing import Optional
from easy_pil import Editor, load_image_async, Font
from PIL import Image, ImageOps
import requests
import re

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/levels.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('INFO')

standard_img = "images/tam.png"
xp_per_message = 20


class Levels(discord.Cog):
	def __init__(self, bot):  # Initialization of levels command
		self.bot = bot

	@discord.Cog.listener()  # Leveling Cog loading
	async def on_ready(self):
		print("Levelling Cog Loaded")
		logger.info('Levelling Cog Loaded')

	@discord.Cog.listener()
	async def on_message(self, message):
		try:
			logger.info('started message')
			if not message.author.bot:
				with open("levels.json", "r") as levels:
					data = json.load(levels)
				if str(message.guild.id) in data:  # Checks if user is in the database
					author = str(message.author.id)  # Defines the author of the message
					if author in data[str(message.guild.id)]:  # If user is in database:
						xp = data[str(message.guild.id)][str(message.author.id)]['xp']
						lvl = data[str(message.guild.id)][str(message.author.id)]['level']
						increased_xp = xp + xp_per_message
						new_level = int(increased_xp / 100)
						data[str(message.guild.id)][str(message.author.id)]['xp'] = increased_xp
						with open("levels.json", "w") as levels:
							json.dump(data, levels, indent = 2)
						if new_level > lvl:
							await message.respond(f'{message.author.mention} Just Levelled Up to Level {new_level}')
							data[str(message.guild.id)][str(message.author.id)]['level'] = new_level
							data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
							with open("levels.json", "w") as levels:
								json.dump(data, levels, indent = 2)
					else:  # Add user to database
						data[str(message.guild.id)] = {}  #
						data[str(message.guild.id)][str(message.author.id)] = {}  #
						data[str(message.guild.id)][str(message.author.id)]['xp'] = 0  # Assigns them 0 level XP
						data[str(message.guild.id)][str(message.author.id)]['level'] = 1  # Assigns level 1
						data[str(message.guild.id)][str(message.author.id)][
							'img'] = standard_img  # Assigns the background image
						data[str(message.guild.id)][str(message.author.id)][
							'color'] = "#ff9933"  # Assigns the standard color for levels
					with open("levels.json", "w") as levels:
						json.dump(data, levels, indent = 2)
				else:
					data[str(message.guild.id)] = message.guild.id
					with open("levels.json", "w") as levels:
						json.dump(data, levels, indent = 2)
		except Exception as error:  # Catch
			logger.exception(error)

	@discord.slash_command(description = "Shows the rank of a user.")
	async def rank(self, ctx: commands.Context, member: Optional[discord.Member]):
		print('rank')
		try:
			logger.info('started rank')
			user = member or ctx.author
			with open("levels.json", "r") as f:
				data = json.load(f)
				xp = data[str(ctx.guild.id)][str(user.id)]["xp"]
				lvl = data[str(ctx.guild.id)][str(user.id)]["level"]
				url = data[str(ctx.guild.id)][str(user.id)]['img']
				text_color = data[str(ctx.guild.id)][str(user.id)]['color']
				next_levelup_xp = (lvl + 1) * 100
				xp_have = data[str(ctx.guild.id)][str(user.id)]["xp"]
				percentage = int((xp_have * 100) / next_levelup_xp)
				if url.startswith("http"):  # Checks for http in the image link
					try:  # Tests the image link
						im = Image.open(requests.get(url, stream = True).raw)
						width, height = im.size
						if width != 900 or height != 300:
							im = ImageOps.fit(im, (900, 300))
					except Exception as e:
						logging.exception(e)
						im = standard_img
						await ctx.respond("Warning: The image link you have chosen is invalid")
				else:
					im = url
				background = Editor(im)
				profile = await load_image_async(str(user.display_avatar.url))
				profile = Editor(profile).resize((150, 150)).circle_image()
				poppins = Font.poppins(size = 40)
				poppins_small = Font.poppins(size = 30)
				ima = Editor("images/black.png")
				background.blend(image = ima, alpha = .5, on_top = False)  # Profile picture
				background.paste(profile.image, (30, 30))  # XP bar if empty
				background.rectangle((30, 220), width = 650, height = 40, fill = '#fff', radius = 20)  # xp bar full
				if percentage > 0:  # avoids ugly line
					background.bar(
						(30, 220),
						max_width = 650,
						height = 40,
						percentage = percentage,
						fill = text_color,
						radius = 20
					)
				background.text((200, 40), str(user.display_name), font = poppins, color = text_color)  # Username placement and coloring
				background.rectangle((200, 100), width = 350, height = 2, fill = text_color)
				background.text(  # XP text data
					(200, 130),
					f'Level : {lvl} ' +
					f'XP : {xp} / {(lvl + 1) * 100}',
					font = poppins_small,
					color = text_color
				)
				card = File(fp = background.image_bytes, filename = "rank.png")  # Creates the image and sends it
				await ctx.respond(file = card)
				logger.info('sent')
		except Exception as error:
			logger.error(error)

	@discord.slash_command(description = "Change the image used in the /rank command.")
	async def image(self, ctx, url):
		try:
			logger.info('started image')
			with open("levels.json", "r") as f:
				data = json.load(f)
			data[str(ctx.guild.id)][str(ctx.author.id)]['img'] = url
			with open("levels.json", "w") as f:
				json.dump(data, f, indent = 2)
			await ctx.respond("New image set!")
		except Exception as error:
			await ctx.respond("Unknown Error")
			logger.exception(error)

	@discord.slash_command(description = "Change the color used in the rank command")
	async def color(self, ctx, set_color):
		try:
			logger.info('started color')
			with open("levels.json", "r") as f:
				data = json.load(f)
			if not set_color.startswith("#"):  # adds # to the start to make it a valid color code
				set_color = f'#{set_color}'
			# checking validity of the hex code
			match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', set_color)
			if match:
				# putting data back into json
				data[str(ctx.guild.id)][str(ctx.author.id)]['color'] = set_color
				with open("levels.json", "w") as f:
					json.dump(data, f, indent = 2)
				await ctx.respond("New colour set!")
			else:
				await ctx.respond("Invalid hex code")
		except Exception as error:
			logger.exception(error)

	@discord.slash_command(description = "Shows the leaderboard.")
	async def leaderboard(self, ctx, range_num = '10'):
		try:
			logger.info('started leaderboard')
			with open("levels.json", "r") as f:
				data = json.load(f)
				l = {}
				for userid in data[str(ctx.guild.id)]:
					xp = int(data[str(ctx.guild.id)][str(userid)]['xp'] + (
							int(data[str(ctx.guild.id)][str(userid)]['level']) * 100))
					l[xp] = f"{userid};{data[str(ctx.guild.id)][str(userid)]['level']};" \
					        f"{data[str(ctx.guild.id)][str(userid)]['xp']}"
				marklist = sorted(l.items(), key = lambda x: x[0], reverse = True)
				l = dict(marklist)
				index = 1
				mbed = discord.Embed(title = "Leaderboard Command Results.")
				for amt in l:
					id_ = int(str(l[amt]).split(";")[0])
					level = int(str(l[amt]).split(";")[1])
					xp = int(str(l[amt]).split(";")[2])

					member = ctx.guild.get_member(id_)

					if member is not None:
						name = member.display_name
						mbed.add_field(name = f"{index}. {name}",
						               value = f"**Level: {level} | XP: {xp}**",
						               inline = False)
					try:
						if index - 1 == int(range_num):
							break
						index += 1
					except:  # all function
						if range_num == 'all' or 'a':
							index += 1
						else:
							range_num = 10
							index += 1

				await ctx.respond(embed = mbed)

		except Exception as error:
			logger.exception(error)


def setup(client):
	client.add_cog(Levels(client))
