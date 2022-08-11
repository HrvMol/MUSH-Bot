from distutils.log import INFO
import discord
import json
import logging
from discord import File
from discord.ext import commands
from typing import Optional
from easy_pil import Editor, load_image_async, Font

from PIL import Image
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

class Levelsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Levelling Cog Loaded")
        logger.info('Levelling Cog Loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.info('started message')
        if not message.author.bot:
            with open("levels.json", "r") as f:
                data = json.load(f)
            
            #checking if user is in database
            if str(message.guild.id) in data:
                if str(message.author.id) in data[str(message.guild.id)]:
                    xp = data[str(message.guild.id)][str(message.author.id)]['xp']
                    lvl = data[str(message.guild.id)][str(message.author.id)]['level']

                    increased_xp = xp + xp_per_message
                    new_level = int(increased_xp/100)

                    data[str(message.guild.id)][str(message.author.id)]['xp'] = increased_xp

                    with open("levels.json", "w") as f:
                        json.dump(data, f, indent=2)

                    if new_level > lvl:
                        await message.channel.send(f'{message.author.mention} Just Levelled Up to Level {new_level}')

                        data[str(message.guild.id)][str(message.author.id)]['level'] = new_level
                        data[str(message.guild.id)][str(message.author.id)]['xp'] = 0

                        with open("levels.json", "w") as f:
                            json.dump(data, f, indent=2)
            
                elif str(message.guild.id) in data:
                    data[str(message.guild.id)][str(message.author.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                    data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                    data[str(message.guild.id)][str(message.author.id)]['img'] = standard_img
                    data[str(message.guild.id)][str(message.author.id)]['color'] = "#ff9933"
                else:
                    data[str(message.guild.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)] = {}
                    data[str(message.guild.id)][str(message.author.id)]['xp'] = 0
                    data[str(message.guild.id)][str(message.author.id)]['level'] = 1
                    data[str(message.guild.id)][str(message.author.id)]['img'] = standard_img
                    data[str(message.guild.id)][str(message.author.id)]['color'] = "#ff9933"

                with open("levels.json", "w") as f:
                    json.dump(data, f, indent=2)
        
    @commands.command(name="rank")
    async def rank(self, ctx: commands.Context, member: Optional[discord.Member]):
        logger.info('started rank')
        user = member or ctx.author
        with open("levels.json", "r") as f:
            data = json.load(f)

            xp = data[str(ctx.guild.id)][str(user.id)]["xp"]
            lvl = data[str(ctx.guild.id)][str(user.id)]["level"]
            url = data[str(ctx.guild.id)][str(user.id)]['img']
            text_color = data[str(ctx.guild.id)][str(user.id)]['color']
            
            next_levelup_xp = (lvl+1)*100
            xp_have = data[str(ctx.guild.id)][str(user.id)]["xp"]
            percentage = int((xp_have*100)/next_levelup_xp)

            #image to use
            if url.startswith("http"):
                try:
                    im = Image.open(requests.get(url, stream=True).raw)
                    width, height = im.size
                    if width != 900 or height != 300:
                        im = standard_img
                        await ctx.send("Warning: The Image you have chosen is not 900 x 300px, please change the size in order for your image to work")
                except:
                    im = standard_img
                    await ctx.send("Warning: The image link you have chosen is invalid")
            else:
                im = url

            background = Editor(im)

            profile = await load_image_async(str(user.avatar_url))
            profile = Editor(profile).resize((150, 150)).circle_image()

            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            ima = Editor("images/black.png")
            background.blend(image=ima, alpha=.5, on_top=False)

            #pfp
            background.paste(profile.image, (30, 30))
            #xp bar empty
            background.rectangle((30,220), width=650, height=40, fill='#fff', radius=20)
            #xp bar full
            if percentage > 0: #avoids ugly line
                background.bar(
                    (30,220),
                    max_width=650,
                    height=40,
                    percentage=percentage,
                    fill=text_color,
                    radius=20
                )
            #username
            background.text((200, 40), str(user.name), font=poppins, color=text_color)
            #divider
            background.rectangle((200, 100), width=350, height=2, fill=text_color)
            #xp data
            background.text(
                (200, 130),
                f'Level : {lvl} '
                + f'XP : {xp} / {(lvl+1)*100}',
                font=poppins_small,
                color=text_color
                )
            #making the image and sending it
            card = File(fp=background.image_bytes, filename="rank.png")
            await ctx.send(file=card)
            logger.info('sent')
    
    @commands.command(name="image")
    async def image(self, ctx, url):
        logger.info('started image')
        with open("levels.json", "r") as f:
            data = json.load(f)
        
        data[str(ctx.author.id)]['img'] = url

        with open("levels.json", "w") as f:
            json.dump(data, f, indent=2)
        await ctx.send("New image set!")

    @commands.command(name="color", aliases=["colour"])
    async def color(self, ctx, set_color):
        logger.info('started color')
        with open("levels.json", "r") as f:
            data = json.load(f)
        
        #adding # to the start
        if not set_color.startswith("#"):
            set_color = f'#{set_color}'

        #checking validity of the hex code
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', set_color)

        if match:
            #putting data back into json
            data[str(ctx.author.id)]['color'] = set_color

            with open("levels.json", "w") as f:
                json.dump(data, f, indent=2)
            await ctx.send("New colour set!")

        else:
            await ctx.send("Invalid hex code")

    @commands.command(name="leaderboard")
    async def leaderboard(self, ctx, range_num=5):
        logger.info('started leaderboard')
        with open("levels.json", "r") as f:
            data = json.load(f)

            l = {}

            for userid in data[str(ctx.guild.id)]:
                print(userid)
                xp = int(data[str(ctx.guild.id)][str(userid)]['xp']+(int(data[str(ctx.guild.id)][str(userid)]['level'])*100))
                print('done xp')
                l[xp] = f"{userid};{data[str(ctx.guild.id)][str(userid)]['level']};{data[str(ctx.guild.id)][str(userid)]['xp']}"
                print('done l')

            marklist = sorted(l.items(), key=lambda x:x[0], reverse=True)
            l = dict(marklist)

            index=1

            mbed = discord.Embed(
            title="Leaderboard Command Results"
            )

            for amt in l:
                print(l[amt])
                id_ = int(str(l[amt]).split(";")[0])
                level = int(str(l[amt]).split(";")[1])
                xp = int(str(l[amt]).split(";")[2])

                member = await self.bot.fetch_user(id_)

                if member is not None:
                    name = member.name
                    mbed.add_field(name=f"{index}. {name}",
                    value=f"**Level: {level} | XP: {xp}**", 
                    inline=False)

                    if index == range_num:
                        break
                    else:
                        index += 1

            await ctx.send(embed = mbed)

def setup(client):
    client.add_cog(Levelsys(client))