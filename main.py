import aiofiles
import discord
from discord.ext import commands
import os
import sys
import socket
import logging

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
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = '!', intents = intents)

if "mush-bot" not in os.getcwd().lower():
	os.chdir(os.getcwd() + "/mush-bot")

TOKEN = os.environ.get('BOT_TOKEN')  # Token allows to sign in to the bot account
bot.join_message = ''


for file in os.listdir('./cogs'):  # Loads cogs from ./cogs folder
	if file.endswith('.py'):
		bot.load_extension("cogs." + file[:-3])
logger = logging.getLogger(__name__)

handler = logging.FileHandler('logs/main.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@bot.event

    if payload.member == bot.user: return
    
    #checks through list to see if reaction is on one of the reaction role messages
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            print("removing role")
            guild = bot.get_guild(payload.guild_id)#gets server react was in
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))#removes role to user that reacted
            return

#command to set up the reaction role
@bot.command()
@commands.has_any_role("Sergeant", "Deputy Commander", "Commander", "Officer", "Discord Admin")
async def react_role(ctx, role: discord.Role=None, msg=None, emoji=None):
    if role != None and msg != None and emoji != None:
        channel = ctx.channel
        msg = await channel.send(msg)#sends message that was an arg of the function
        await msg.add_reaction(emoji)#adds emoji to message
        emoji_utf = str(emoji.encode("utf-8"))#encodes emoji as txt files cannot use emojis
        bot.reaction_roles.append((role.id, msg.id, emoji_utf))#appends to runtime reaction list

        async with aiofiles.open("reaction_roles.txt", mode = "a") as file:
            await file.write(f"{role.id} {msg.id} {emoji_utf}\n")#appends the new data to text file for permanent storage

    else:
        await ctx.send("invalid arguments")
    
    await ctx.message.delete()#remove user command message


# ---------------------WELCOME MESSAGE-------------------- #
@bot.event
async def on_member_join(ctx):
	try:  # Sends message in new members in mush, if test bot, then test server channel
		try:
			join_channel = await bot.fetch_channel(970370019701690468)  # New members chat in mush
		except: # too broad, breaks the message sending in the right server
			join_channel = await bot.fetch_channel(993562809994584197)  # New members chat in test server

		await join_channel.send(f'{ctx.mention}\n {bot.join_message}')
	except Exception as error:
		logger.error(error)

#----------------------TEST COMMAND----------------------#

@bot.slash_command(description="test if the bot is working")
async def test(ctx):
    await ctx.respond("Operational")

bot.run(TOKEN)