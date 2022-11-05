import logging
import os
import socket
import sys
import aiofiles
import discord
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("TOKEN"))

if sys.platform == "linux":
	try:
		s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		s.bind('\0postconnect_gateway_notify_lock')
	except socket.error as e:
		error_code = e.args[0]
		error_string = e.args[1]
		print("Process already running (%d:%s ). Exiting" % (error_code, error_string))
		sys.exit(0)

# Bot intent commands for basic prefixing
bot = discord.Bot(command_prefix='.')

if "mush-bot" not in os.getcwd().lower():
	os.chdir(os.getcwd() + "/mush-bot")

TOKEN = os.environ.get('BOT_TOKEN')  # Token allows to sign in to the bot account
bot.join_message = ''

cogs_list = []

for cog in os.listdir('./cogs'):  # Loads cogs from ./cogs folder
	if cog.endswith('.py'):
		cog = os.path.splitext(cog)
		cog = cog[0]
		cogs_list.append(cog)

for cog in cogs_list:
	bot.load_extension(f'cogs.{cog}')

logger = logging.getLogger(__name__)

handler = logging.FileHandler('logs/main.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# ------------------------BOT SETUP----------------------- #
@bot.event
async def on_ready():
	async with aiofiles.open("join_message.md", mode = "a"):  # Creates join_message text file if not already existing
		pass
	async with aiofiles.open("join_message.md", mode = "r") as join_message:
		# Reads join_message file and puts data into join_message list
		bot.join_message = await join_message.read()
	try:
		async with aiofiles.open("cogs/help.md", mode = "r") as help_message:
			bot.help = await help_message.read()
	except Exception as error:
		logging.exception(error)
		pass
	print("Logged in and ready")


# ---------------------WELCOME MESSAGE-------------------- #
@bot.event
async def on_member_join(member):
	for channel in member.guild.channels:
		if channel == 970370019701690468:
			await channel.send(f'{member.mention}\n {bot.join_message}')


# ----------------------TEST COMMAND---------------------- #
@discord.slash_command(name = "test", description = "Tests if the bot is working")
async def test(ctx):
	await ctx.respond("Bot is operational")

bot.run(token)
