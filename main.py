import aiofiles
import discord
from discord.ext import commands

#bot intents to allow for reaction roles
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

#token allows to sign in to the bot account
TOKEN = 'NzU3MzIzNDkxNTUxNzM5OTY0.Ga58ok.Fld12BrMlNwyWnPDOKMWtt_g187A51A9DtC_rc'

#list of reaction roles data
bot.reaction_roles = []

bot.join_message = ''

#on boot function
@bot.event
async def on_ready():
    #creates reaction_roles text file if not already existing
    async with aiofiles.open("reaction_roles.txt", mode="a") as temp:
        pass

    #reads reaction roles file and puts data into reaction_roles list
    async with aiofiles.open("reaction_roles.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))

    #creates join_message text file if not already existing
    async with aiofiles.open("join_message.txt", mode="a") as temp:
        pass

    #reads join_message file and puts data into join_message list
    async with aiofiles.open("join_message.txt", mode="r") as file:
        bot.join_message = await file.read()

    print("logged in and ready")

#---------------------REACTION ROLES---------------------#

@bot.event
async def on_raw_reaction_add(payload):
    #check for if user reacting is bot so it can be ignored
    if payload.member == bot.user:
        return

    #checks through list to see if reaction is on one of the reaction role messages
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            print("adding role")
            guild = bot.get_guild(payload.guild_id)#gets server react was in
            await payload.member.add_roles(guild.get_role(role_id))#adds role to user that reacted
            return

@bot.event
async def on_raw_reaction_remove(payload):
    #check for if user reacting is bot so it can be ignored
    if payload.member == bot.user:
        return
    
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

#---------------------WELCOME MESSAGE--------------------#

@bot.event
async def on_member_join(member):
    await member.send(bot.join_message)
