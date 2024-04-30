# (C) Copyright Cyrus#8000 / cyshe
# Source : https://github.com/CyrusSE/Discord-GrowtopiaBot/

import asyncio
import discord, datetime, time
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import os.path
from os import system
import time
from time import sleep
#from webserver import keep_alive
import sys
from discord.ext.commands import cooldown, BucketType
import json
import patoolib
from io import StringIO
import glob
from random import choice
from discord.utils import get
from bs4 import BeautifulSoup
import requests
import ipaddress 
from fuzzywuzzy import fuzz
import threading
import re
from urllib.parse import quote_plus
import random
import datetime
import subprocess

start_time = time.time()
bot = commands.Bot(command_prefix=("!"), allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True), intents = discord.Intents.all(), help_command=None)
os.system('cls')
bot.up = round(datetime.datetime.now().timestamp())
bot.clown = None
bot.autodelete = None
bot.serverstatus = True
online_users_counter = 0
previous_activity_name = ""


def is_utf8(text):
    try:
        text.encode('latin1').decode('utf-8-sig')
        return True
    except:
        return False

def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

async def get_online_users():
    global previous_activity_name
    url = 'https://privategt.com/online/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        result = requests.get(url, headers=headers, verify=True)
        result = result.content.decode()
    except requests.exceptions.SSLError:
        print("SSL Error encountered")
        result = "Error???"
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        result = "Error???"
    return result

def unix_to_date(unix_timestamp):
    datetime_obj = datetime.datetime.fromtimestamp(unix_timestamp)
    time_diff = datetime.datetime.now() - datetime_obj
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    if days > 0:
        time_str = f"{days} days ago"
    elif hours > 0:
        time_str = f"{hours} hours ago"
    else:
        time_str = f"{minutes} minutes ago"

    return time_str


async def update_status():
    global online_users_counter, previous_activity_name
    await bot.wait_until_ready()
    status_type = discord.Status.online 
    while not bot.is_closed():
        online_users = await get_online_users()
       # print(online_users)
        activity_name = f"{online_users} people online"
        if online_users_counter >= 5:
            activity_name2 = "SERVER IS DOWN"
            status_type = discord.Status.dnd
            try:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name2), status=status_type)
                if bot.serverstatus == True:
                    channel = bot.get_channel(1030821861921136710)
                    await channel.send(f"Server has been detected DOWN!")
                    channel2 = bot.get_channel(1030821921639641160)
                    await channel2.send("Server has been detected DOWN!")
                    bot.serverstatus = False
            except:
                print("Connection to Discord closed. Retrying...")
        else:
            activity_name = f"{online_users} people online"
            if status_type == discord.Status.online:
                status_type = discord.Status.idle
            else:
                status_type = discord.Status.online

        if activity_name == previous_activity_name:
            online_users_counter += 1
            channel = bot.get_channel(1113504703846809712)
            await channel.send(f"Detected same {online_users_counter} old {activity_name} new {previous_activity_name}")
        else:
            online_users_counter = 0
            activity_name = f"{online_users} people online"
            try:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_name), status=status_type)
                if bot.serverstatus == False:
                  channel = bot.get_channel(1030821861921136710)
                  await channel.send("Server has been detected UP!")
                  channel2 = bot.get_channel(1030821921639641160)
                  await channel2.send("Server has been detected UP!")
                  bot.serverstatus = True
            except:
                print("Connection to Discord closed. Retrying...")
        activity_name = f"{online_users} people online"
        previous_activity_name = activity_name
        await asyncio.sleep(3)

def print_item_with_border(item_name, amount, value):
    total_length = max(len(item_name), len(value)) + 6
    border = '═' * total_length
    line = f'╠{border}╣  {item_name}  ╠{border}╣'

    print(f'╔{border}╦{"═" * 9}╦{border}╗')
    print(line)
    print(f'╠{border}╣  Amount: {amount}  ╠{border}╣')
    print(f'╠{border}╣  Value: {value}  ╠{border}╣')
    print(f'╚{border}╩{"═" * 9}╩{border}╝')
    print()

def parse_price(price):
    if "!updateprice" in price:
        print("Invalid price: " + price)
        return "Invalid price"
    if "/" in price:
        numbers = re.findall(r'\d+', price)
        numbers = [int(num) for num in numbers]
        highest_number = max(numbers)
        return highest_number
    match = re.search(r'(\d+)-?(\d*)\s*(\w+)', price)
    if match:
        lower = int(match.group(1))
        higher = int(match.group(2)) if match.group(2) else lower
        unit = match.group(3).lower()
        if unit == "diamond":
            unit = "world"
            lower *= 100
            higher *= 100
        elif unit == "blue":
            unit = "world"
            lower *= 10000
            higher *= 10000
        if higher > lower:
            return higher
        else:
            return lower
    else:
        print("Incorrect price: " + price)
        return "Incorrect price"

def convert_to_locks(value):
    if value < 100:
        return f"{value} World Locks"
    elif value < 10000:
        return f"{round(value/100):.0f} Diamond Locks"
    else:
        return f"{round(value/10000):.0f} Blue Gem Locks"

    # last_online = cells[1].get_text()
    # player_name = cells[2].get_text()
    # email = cells[3].get_text()
    # last_ip = cells[4].get_text()
    # mac = cells[5].get_text()
    # gtps_wls = cells[6].get_text()
    # twofa = cells[7].get_text()
    # rid = cells[8].get_text()
    # xp_lvl = cells[9].get_text()
    # gems = cells[10].get_text()
    # status = cells[11].get_text()
    # banned = cells[12].get_text()
    # banned_by = cells[13].get_text()
    # banned_for = cells[14].get_text()
    # ban_expires = cells[15].get_text()


#example usage print(table_data[0]['email'])
def getdata(growid):
    url = ("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php")
    r = requests.post(url, data={'first_name': growid})
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        return None
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.find_all('tr', class_='list')
    data = []
    for row in rows:
        row_data = {}
        row_data['last_online'] = row.find_all('td')[1].text.strip()
        row_data['player_name'] = row.find_all('td')[2].text.strip()
        row_data['email'] = row.find_all('td')[3].text.strip()
        row_data['last_ip'] = row.find_all('td')[4].text.strip()
        row_data['mac'] = row.find_all('td')[5].text.strip()
        row_data['gtps_wls'] = row.find_all('td')[6].text.strip()
        row_data['fa'] = row.find_all('td')[7].text.strip()
        row_data['rid'] = row.find_all('td')[8].text.strip()
        row_data['xp_lvl'] = row.find_all('td')[9].text.strip()
        row_data['gems'] = row.find_all('td')[10].text.strip()
        row_data['status'] = row.find_all('td')[11].text.strip()
        row_data['banned'] = row.find_all('td')[12].text.strip()
        if row_data['banned'] == "Yes":
            row_data['banned_by'] = row.find_all('td')[13].text.strip()
            row_data['banned_for'] = row.find_all('td')[14].text.strip()
            row_data['ban_expires'] = row.find_all('td')[15].text.strip()
        else:
            row_data['banned_by'] = "None"
            row_data['banned_for'] = "None"
            row_data['ban_expires'] = "None"
        data.append(row_data)

    return data[0] if data else None

@bot.event
async def on_ready():
    print(f'''Logged In As {bot.user}#{bot.user.discriminator}''')
    with open('files/status.txt', 'r') as y:
        s = y.read()
        if 'online' in s:
            await bot.change_presence(status=discord.Status.online)
        elif 'idle' in s:
            await bot.change_presence(status=discord.Status.idle)
        elif 'dnd' in s:
            await bot.change_presence(status=discord.Status.dnd)
        elif 'offline' in s:
            await bot.change_presence(status=discord.Status.offline)
        else:
            with open('files/status.txt', 'w') as s:
                s.write('online')
                
@bot.event
async def on_message(message):
  if message.channel.id == 1063539200193986630:
    return
  if message.guild is None:
    if message.content.startswith("!recovery") or message.content.startswith("!verify"):
      guild = bot.get_guild(742792944079208540)
      if guild.get_member(message.author.id) is not None:
          await bot.process_commands(message)
          return
      else:
          await message.channel.send("Due to security concerns, this feature can only be used if you are in our Main Server.\nJoin us https://discord.com/invite/gtps3")
          return
    else:
      return
  if message.guild != None:
    # if message.channel.id == 918522194798215239 or message.channel.id == 983333006708191246 or message.channel.id == 767108013752320020 or message.channel.id == 1059112511967871036 or message.channel.id == 869619078820659210:
    #   if message.content == "<@830229763171418163>":
    #     await message.reply("Hello there! If you need assistance, please type **!commands** to view the list of available commands.")
    #     return
    #   if message.content == "!commands":
    #     embed=discord.Embed(description="**!recovery <GrowID> <Email>**\n╰▸ This command will help you to recovery your account, and only working in DM.\n\n**!verify <GrowID> <Email>**\n╰▸ This command will help you to join to our Mod Server, and only working in DM.\n\n**!checkprice <Name Item>**\n╰▸ This command will send you the price of an item you asked for.\n\n**!sugguestprice <Name Item>**\n╰▸ This command is intended for suggesting price changes to items that are listed in ``!checkprice``. This allows our staff to review and update pricing information as needed, ensuring that our users have access to accurate and up-to-date pricing information.\n\n**!myvalue**\n╰▸ This command displays the net worth of your account, considering both tradeable and untradeable items, based on the prices obtained from the ``!checkprice`` command.\n\n**!hostpc**\n╰▸ This command will send you a tutorial how to play GTPS 3 on pc in simplest way and also with video.\n\n**!hostandroid**\n╰▸ This command will send you android host file.\n\n**!hostios**\n╰▸ This command will send you ios host link.", color=discord.Colour.random())
    #     embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
    #     embed.set_author(name="Command List", icon_url=f"{message.author.avatar}")
    #     embed.set_footer(text="Join us https://discord.com/invite/gtps3 !")
    #     await message.reply(embed=embed)
    #   allowed = {"!checkprice", "!hostpc", "!hostandroid", "!hostios"}
    #   for i in allowed:
    #     if message.content.startswith(i):
    #       await bot.process_commands(message)
    #       return
    if message.guild.id == 742792944079208540 or message.guild.id == 771352967277182976 or message.guild.id == 846341020286451732 or message.guild.id == 899948087387242526 or message.guild.id == 945518703703912518 or message.guild.id == 983333006708191243 or message.guild.id == 1113163119573880933:
      if message.content == "<@830229763171418163>":
        await message.channel.send("Hello there! If you need assistance, please type **!commands** to view the list of available commands.")
        return
      if message.content == "!commands":
        if message.channel.id == 918522194798215239 or message.channel.id == 983333006708191246 or message.channel.id == 767108013752320020 or message.channel.id == 1059112511967871036 or message.channel.id == 869619078820659210:
          embed=discord.Embed(description="\n**Important Links:**\n**[GTPS3 Server](https://discord.com/invite/gtps3) | [Invite GTPS3 Bot](https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot)**\n\n**!recovery <GrowID> <Email>**\n╰▸ This command will help you to recovery your account, and only working in DM.\n\n**!verify <GrowID> <Email>**\n╰▸ This command will help you to join to our Mod Server, and only working in DM.\n\n**!checkprice <Name Item>**\n╰▸ This command will send you the price of an item you asked for.\n\n**!suggestprice <Name Item>**\n╰▸ This command is intended for suggesting price changes to items that are listed in ``!checkprice``. This allows our staff to review and update pricing information as needed, ensuring that our users have access to accurate and up-to-date pricing information.\n\n**!myvalue**\n╰▸ This command displays the net worth of your account, considering both tradeable and untradeable items, based on the prices obtained from the ``!checkprice`` command.\n\n**!hostpc**\n╰▸ This command will send you a tutorial how to play GTPS 3 on pc in simplest way and also with video.\n\n**!hostandroid**\n╰▸ This command will send you android host file with Virutal Host.\n\n**!hostandroid2**\n╰▸ This command will send you android host file with Host Go.\n\n**!hostios**\n╰▸ This command will send you ios host link.\n\n**!invite**\n╰▸ This command will send you GTPS 3 Discord link and GTPS 3 Bot invite link.", color=discord.Colour.random())
          #embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
          embed.set_author(name="Command List", icon_url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
          embed.set_footer(text="Join us https://discord.com/invite/gtps3 !")
          await message.channel.send(embed=embed)
          return
        else:
          await message.channel.send("Please use this command in bot-commands channel only or you can invite this bot and use it in your server.")
          return
      await bot.process_commands(message)
    else:
      if message.channel.id == 1101568951848271973:
        if message.author.id == 420584968566079508:
          await bot.process_commands(message)
      if message.content.startswith("!suggestprice"):
        await message.channel.send("Due to security concerns, this feature can only be used in our Main Server.\nJoin us https://discord.com/invite/gtps3")
        return
      if message.content == "<@830229763171418163>":
        await message.channel.send("Hello there! If you need assistance, please type **!commands** to view the list of available commands.")
        return
      if message.content == "!commands":
        embed=discord.Embed(description="\n**Important Links:**\n**[GTPS3 Server](https://discord.com/invite/gtps3) | [Invite GTPS3 Bot](https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot)**\n\n**!recovery <GrowID> <Email>**\n╰▸ This command will help you to recovery your account, and only working in DM.\n\n**!verify <GrowID> <Email>**\n╰▸ This command will help you to join to our Mod Server, and only working in DM.\n\n**!checkprice <Name Item>**\n╰▸ This command will send you the price of an item you asked for.\n\n**!suggestprice <Name Item>**\n╰▸ This command is intended for suggesting price changes to items that are listed in ``!checkprice``. This allows our staff to review and update pricing information as needed, ensuring that our users have access to accurate and up-to-date pricing information.\n\n**!myvalue**\n╰▸ This command displays the net worth of your account, considering both tradeable and untradeable items, based on the prices obtained from the ``!checkprice`` command.\n\n**!hostpc**\n╰▸ This command will send you a tutorial how to play GTPS 3 on pc in simplest way and also with video.\n\n**!hostandroid**\n╰▸ This command will send you android host file with Virutal Host.\n\n**!hostandroid2**\n╰▸ This command will send you android host file with Host Go.\n\n**!hostios**\n╰▸ This command will send you ios host link.\n\n**!invite**\n╰▸ This command will send you GTPS 3 Discord link and GTPS 3 Bot invite link.", color=discord.Colour.random())
       # embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
        embed.set_author(name="Command List", icon_url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
        embed.set_footer(text="Join us https://discord.com/invite/gtps3 !")
        await message.channel.send(embed=embed)
        return
      if message.author.id == 567561637951832083:
        await bot.process_commands(message)
        return
      if message.content.startswith("!suggestprice"):
        await message.channel.send("Due to security concerns, this feature can only be used in our Main Server.\nJoin us https://discord.com/invite/gtps3")
        return
      if message.content == "!myvalue":
        if message.guild.id == 1061469032408158218:
          await bot.process_commands(message)
          return
        await message.channel.send("This command can only be running in bot-command on GTPS3 Main Server.\nJoin us https://discord.com/invite/gtps3")
        return
      if message.content.startswith("!recovery") or message.content.startswith("!verify"):
        await message.channel.send("This command can only be running in <@830229763171418163> DM.")
        return
      allowed = {"!checkprice", "!hostpc", "!hostandroid", "!hostandroid2", "!hostios", "!invite"}
      for i in allowed:
        if message.content.startswith(i):
          await bot.process_commands(message)
          break

@bot.event
async def on_member_join(member):
    #print(f"{member} {member.guild.id}")
  # if member.guild.id == 742792944079208540:
    if member.guild.id == 742792944079208540:
      vyte = await bot.fetch_user(778531285945417738)
      channel = bot.get_channel(767108013752320020)
      guild = bot.get_guild(742792944079208540)
      guild2 = bot.get_guild(899948087387242526)
      if member.id == vyte.id:
        return
      if member.name.lower() == vyte.name.lower():
        await channel.send(f"{member.name}#{member.discriminator}({member.id}) just joined and impersonating {vyte.name}#{vyte.discriminator}")
        await channel.send(f"Auto banned {member.name}#{member.discriminator}")
        await guild.ban(member)
        await channel.send(f"Auto banned {member} [Download Server]")
        await guild2.ban(member)
        return
      if "vyte" in member.name.lower():
        await channel.send(f"{member.name}#{member.discriminator}({member.id}) just joined and has {vyte.name} in his name")
      if member.id == vyte.id:
        return
      #if "del" in member.name.lower():
        #await channel.send(f"{member.name}#{member.discriminator}({member.id}) just joined and has {delid.name} in his name")
      chris = await bot.fetch_user(514394370804285460)
      if member.name.lower() == chris.name.lower():
        if time.time() - member.created_at.timestamp() < 1728000:
          await channel.send(f"[New account] {member.name}#{member.discriminator}({member.id}) just joined and impersonating {chris.name}#{chris.discriminator}")
          await guild.ban(member)
          await channel.send(f"Auto banned {member} [Download Server]")
          await guild2.ban(member)
          return
      if "christopher" in member.name.lower():
        if time.time() - member.created_at.timestamp() < 1728000:
          await channel.send(f"[New account] {member.name}#{member.discriminator}({member.id}) just joined and has {chris.name} in his name")
    if member.guild.id == 771352967277182976:
        ww = os.path.exists(f"verified\{member.id}_.txt")
        if ww == True:
          oo = open(f"verified\{member.id}_.txt", "r")
          yy = oo.read()
          if yy == member.name:
            nicks = ''.join(choice((str.upper, str.lower))(c) for c in yy)
            await member.edit(nick=nicks)
          else: 
            await member.edit(nick=yy)
          role = get(member.guild.roles, name="Mod")
          await member.add_roles(role)
          channel = bot.get_channel(846249905441341441)
          await channel.send(f" <@{member.id}> make sure read these mentioned **channels** <#771352967475363856> <#771352967475363857>")
          log = bot.get_channel(1026125040430891018)
          await log.send(f"Verified <@{member.id}>({member.id}) with growid {yy}.")
        else:
          vchannel = bot.get_channel(771352967277182984)
          await vchannel.send(f"<@{member.id}>, You are not invited by bot, leave from this server and use ``!verify`` command.", delete_after=15)
          log = bot.get_channel(1026125040430891018)
          await log.send(f"Non registered user joined <@{member.id}>({member.id}).")
          return
      

@bot.event
async def on_user_update(user, after):
  guild = bot.get_guild(742792944079208540)
  if guild is not None:
    guild = bot.get_guild(742792944079208540) 
    guild2 = bot.get_guild(899948087387242526)
    vyte = await bot.fetch_user(778531285945417738)
    channel = bot.get_channel(767108013752320020)
    if user.id == vyte.id:
      return
    if after.name.lower() == vyte.name.lower():
      await channel.send(f"{after.name}#{after.discriminator}({after.id}) just changed his name to {after.name}")
      await channel.send(f"Auto banned {after}")
      await guild.ban(user)
      await channel.send(f"Auto banned {after} [Download Server]")
      await guild2.ban(user)
      return
    if "vyte" in after.name.lower():
      await channel.send(f"{after.name}#{after.discriminator}({after.id}) just changed name and has {vyte.name} in his name")
    channel = bot.get_channel(767108013752320020)
    if user.id == vyte.id:
      return
    chris = await bot.fetch_user(514394370804285460)
    if user.id == chris.id:
      return
    if after.name.lower() == chris.name.lower():
      if time.time() - user.created_at.timestamp() < 1728000:
        await channel.send(f"[New account] {after.name}#{after.discriminator}({after.id}) just changed his name to {after.name}")
        await channel.send(f"Auto banned {after}")
        await guild.ban(user)
        await channel.send(f"Auto banned {after} [Download Server]")
        await guild2.ban(user)
        return
    if "christopher" in after.name.lower():
      if time.time() - user.created_at.timestamp() < 1728000:
        await channel.send(f"[New account] {after.name}#{after.discriminator}({after.id}) just changed name has {chris.name} in his name and new account")

@bot.command()
async def restart(ctx):
    if ctx.message.author.id == 567561637951832083:
      await ctx.send("Restart the bot?")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        await ctx.send('Restarting')
        restart_bot()
        return
      elif msg.content == "y":
        await ctx.send('Restarting')
        restart_bot()
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

class MyView(discord.ui.View):
    @discord.ui.button(label="Suggest this item price.", style=discord.ButtonStyle.success)
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("Wtf!")

@bot.command()
async def unbangrowid(ctx, growid = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #velTrue
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 751857959625293995: #cmol
       True
      elif ctx.message.author.id == 904800082480734209: #taco
       True
      elif ctx.message.author.id == 611436125680041986: #lose
       True
      elif ctx.message.author.id == 792897995812765728:
       True
      elif ctx.message.author.id == 976055468420108340: #HOPE
       True
      elif ctx.message.author.id == 616035263692406796: #mrftank
       True
      elif ctx.message.author.id == 913497847838703658: #Cyrio
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      await ctx.send(f"Are you sure you want to **unban** \"{growid}\"? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content.lower() == "yes":
        data = getdata(growid)
        if data is None:
          await ctx.send("Player is not exist.")
          return
        statusban = data['banned']
        if statusban == "Yes":
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'unban': 1})
          by = data['banned_by']
          reason = data['banned_for']
          expire = data['ban_expires']
          await ctx.send(f"Unbanned GrowID {growid} and player was banned by {by} for {reason} ban expires {expire}.")
          channel = bot.get_channel(983333089776390164)
          await channel.send(f"[LOGS] User {ctx.message.author} unbanned {growid} and was banned by {by} for {reason}")
          return
        else:
          await ctx.send(f"GrowID {growid} is not banned.")
          return
      elif msg.content.lower() == "y":
        data = getdata(growid)
        if data is None:
          await ctx.send("Player is not exist.")
          return
        statusban = data['banned']
        if statusban == "Yes":
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'unban': 1})
          by = data['banned_by']
          reason = data['banned_for']
          expire = data['ban_expires']
          await ctx.send(f"Unbanned GrowID {growid} and player was banned by {by} for {reason} ban expires {expire}.")
          channel = bot.get_channel(983333089776390164)
          await channel.send(f"[LOGS] User {ctx.message.author} unbanned {growid} and was banned by {by} for {reason}")
          return
        else:
          await ctx.send(f"GrowID {growid} is not banned.")
          return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

@bot.command()
async def fetchdata(ctx, growid):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.author.id == 514394370804285460:
        True
      elif ctx.message.author.id == 746620014039138405:
        True
      elif ctx.message.author.id == 710537571276554283:
        True
      elif ctx.message.author.id == 420584968566079508:
        True
      elif ctx.message.author.id == 338130528538460160:
        True
      elif ctx.message.author.id == 792897995812765728:
        True
      elif ctx.message.author.id == 321507929289261057:
        True
      elif ctx.message.author.id == 611436125680041986:
        True
      elif ctx.message.author.id == 616523087223062529:
        True
      elif ctx.message.author.id == 751857959625293995:
        True
      else:
        return
      aw = open("files/update.txt", "r")
      awr = aw.read()
      await ctx.send(f"Using ``new`` or ``old`` <t:{awr}:R> data?")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=15)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content.lower() == "new":
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid})
          if r.status_code == 200:
            True
          else:
            await ctx.send("New data is currently unavailable.")
          soup = BeautifulSoup(r.text, features='html.parser')
          values = [item.text.strip() for item in soup.select('.list')]
          if "Player was not found" in str(r.text):
            await ctx.send("Player is not exist.")
            return
          for ss in list(values):
            x = ss.split()
          last = x[1]
          name = x[2]
          email = x[3]
          ip = x[4]
          mac = x[5]
          fa = x[7]
          rid = x[8]
          lvl = x[9]
          statusban = x[12]
          banned = "False"
          reason = "False"
          long = "False"
          await ctx.send(f"Name : {name}, XP/Level {lvl}, ip {ip}, mac {mac}, rid {rid}, Banned by and how long : {banned}, (last online {last})")
          if statusban == "Yes":
              banned = x[13]
          asd = os.path.exists(f"players\{growid}_.json")
          if asd == True:
            data2 = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
            rawip = data2["ip"]
            rawmac = data2["mac"]
            rawemail = data2["email"]
            if "2fa" in data2:
              raw2fa = data2["2fa"]
            if "rid" in data2:
              rawrid = data2["rid"]
            same = []
            different = []
            if ip == rawip:
                same.append("IP")
            else:
                different.append("IP")
            if mac == rawmac:
                same.append("MAC")
            else:
                different.append("MAC")
            if rid == rawrid:
                same.append("RID")
            else:
                different.append("RID")
            if str(fa) == str(raw2fa):
                same.append("2FA")
            else:
                different.append("2FA")
            if email == rawemail:
                same.append("EMAIL")
            else:
                different.append("EMAIL")
            same_message = "Same : " + ", ".join(same) if same else "Same: None"
            different_message = "Different : " + ", ".join(different) if different else "Different: None"
            await ctx.send(f"{same_message}\n{different_message}\nCompared with <t:{awr}:R> data.")
            await ctx.send(f"Name : {name}, XP/Level {lvl}, ip {ip}, mac {mac}, rid {rid}, Banned by and how long : {banned}, (last online {last})")
      elif msg.content.lower() == "old":
          asd = os.path.exists(f"players\{growid}_.json")
          if asd == True:
              data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
              name = data["name"]
              level = data["level"]
              ip = data["ip"]
              mac = "no mac"
              banned = data["b_b"]
              reason = data["b_r"]
              long = data["b_s"]
              isbanned = banned
              isreason = reason
              islong = long
              if banned == "":
                isbanned = "False"
              if isreason == "":
                isreason = "False"
              if long == "0":
                islong = "False"
              if "mac" in data:
                mac = data["mac"]
              rid = "no rid"
              if "rid" in data:
                rid = data["rid"]
              bgl = "No bgl"
              dl = "No DL"
              data2 = str(data)
              if "7188" in data2:
                bgl = "Has BGL"
              if "1796" in data2:
                dl = "Has DL"
              last = data["lo"]
              await ctx.send(f"Name : {name}, level {level}, ip {ip}, mac {mac}, rid {rid}, Banned : {isbanned}, Reason {reason}, how long {islong}, (BGL : {bgl}, DL : {dl}), (last online {last})")
              await ctx.send(f"Data players last update <t:{awr}:R>")
              return
          else:
              await ctx.send("Cant find that growid")
              aw = open("files/update.txt", "r")
              awr = aw.read()
              await ctx.send(f"Data players last update <t:{awr}:R>")
              return
      else:
           await ctx.send("Only ``new`` or ``old``.")
           return
      #asd = os.path.exists(f"players\{growid}_.json")
    #  if asd == True:
     #   data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
    #  else:
     #   await ctx.send("Cant find that growid")
      #  aw = open("update.txt", "r")
       # awr = aw.read()
        #await ctx.send(f"Data players last update <t:{awr}:R>")
       # return

@bot.command()
async def removerole(ctx, growid = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 751857959625293995: #cmol
       True
      elif ctx.message.author.id == 904800082480734209: #taco
       True
      elif ctx.message.author.id == 611436125680041986: #lose
       True
      elif ctx.message.author.id == 792897995812765728:
       True
      elif ctx.message.author.id == 976055468420108340: #HOPE
       True
      elif ctx.message.author.id == 616035263692406796: #mrftank
       True
      elif ctx.message.author.id == 913497847838703658: #Cyrio
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      await ctx.send(f"Are you sure you want to remove **role** \"{growid}\"? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content.lower() == "yes":
        data = getdata(growid)
        if data is None:
           await ctx.send("Player is not exist.")
           return
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'status': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        statusban = data['banned']
        if statusban == "Yes":
            status = "**Banned**"
            by = data['banned_by']
            reason = data['banned_for']
            expire = data['ban_expires']
            await ctx.send(f"Removed roles GrowID {growid} and player status is **Banned** by {by} for {reason} ban expires {expire}.")
        else:
            await ctx.send(f"Removed roles GrowID {growid} and player status is **Not-Banned**.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed roles {growid}")
        return
      elif msg.content.lower() == "y":
        data = getdata(growid)
        if data is None:
           await ctx.send("Player is not exist.")
           return
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'status': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        statusban = data['banned']
        if statusban == "Yes":
            status = "**Banned**"
            by = data['banned_by']
            reason = data['banned_for']
            expire = data['ban_expires']
            await ctx.send(f"Removed roles GrowID {growid} and player status is **Banned** by {by} for {reason} ban expires {expire}.")
        else:
            await ctx.send(f"Removed roles GrowID {growid} and player status is **Not-Banned**.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed roles {growid}")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

@bot.command()
async def removegems(ctx, growid = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      await ctx.send(f"Are you sure you want to remove **gems** \"{growid}\"? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'gems': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Removed gems GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed gems {growid}")
        return
      elif msg.content == "y":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'gems': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Removed gems GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed gems {growid}")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

def scanplayer(namanya, channel, userid, playerip, playerrid, playermac):
    path = './players'
    bot.track = True
    wkwk = 0
    pop = ""
  #  start_time = time.time()
    for filename in glob.glob(os.path.join(path, '*_.json')):
        try:
            data = json.load(open(filename, encoding='utf-8-sig'))
            # print(filename)
            name = data["name"]
            level = data["level"]
            gems = data["gems"]
            if "rid" in data:
                datarid = data["rid"]
            ip = data["ip"]
            datamac = "no mac"
            if "mac" in data:
                datamac = data["mac"]
            banned = data["b_b"]
            reason = data["b_r"]
            long = data["b_s"]
            isbanned = banned
            isreason = reason
            islong = long
            if banned == "":
                isbanned = "False"
            #else:
                #if ignorebanned == True:
                #  continue
            if isreason == "":
                isreason = "False"
            if long == "0":
                islong = "False"
            bgl = "No bgl"
            dl = "No DL"
            data2 = str(data)
            if "7188" in data2:
                bgl = "Has BGL"
            if "1796" in data2:
                dl = "Has DL"
            last = data["lo"]
            playername = ""
            if bot.track == True:
                if playerrid == datarid:
                    wkwk = wkwk + 1
                    if playerrid == "01A06FF906FBDF2509E170640E2FD48D":
                      continue
                    if banned == "":
                        done = (f"{wkwk}. Player **{name}** and level {level} [SAME RID]. (last online {last})\n")
                        pop += done
                    else:
                        done = (f"{wkwk}. Player **{name}** and level {level} [BANNED by {isbanned} for {reason} how long {islong}] [SAME RID]. (last online {last})\n")
                        pop += done
                    playername = data["name"]
                if playerip == ip:
                    if name == playername:
                      continue
                    wkwk = wkwk + 1
                    if banned == "":
                        done = (f"{wkwk}. Player **{name}** and level {level} [SAME IP]. (last online {last})\n")
                        pop += done
                    else:
                        done = (f"{wkwk}. Player **{name}** and level {level} [BANNED by {isbanned} for {reason} how long {islong}] [SAME IP]. (last online {last})\n")
                        pop += done
                    playername = data["name"]
                if playermac != "02:00:00:00:00:00":
                    if playermac == datamac:
                        if name == playername:
                          continue
                        wkwk = wkwk + 1
                        if banned == "":
                            done = (f"{wkwk}. Player **{name}** and level {level} [SAME MAC]. (last online {last})\n")
                            pop += done
                        else:
                            done = (f"{wkwk}. Player **{name}** and level {level} [BANNED by {isbanned} for {reason} how long {islong}] [SAME MAC]. (last online {last})\n")
                            pop += done
        except Exception as e2:
            print(f"{filename} showalt error")
            continue
 #   end_time = time.time()
  #  elapsed_time = end_time - start_time
  #  asyncio.run_coroutine_threadsafe(channel.send("Took {:.3f} seconds.".format(elapsed_time)), bot.loop)
    aw = open("files/update.txt", "r")
    awr = aw.read()
    dones = (pop)
    dones = dones.replace("`6", "")
    dones = dones.replace("`0", "")
    dones = dones.replace("`9", "")
    dones = dones.replace("`", "")
    dones = dones.replace("**", "")
    s = StringIO()
    s.write(dones)
    s.seek(0)
    if len(pop) < 1999:
        asyncio.run_coroutine_threadsafe(channel.send(f"Found {wkwk} accounts.\n{dones}"), bot.loop)
    else:
        asyncio.run_coroutine_threadsafe(channel.send(f"Found {wkwk} accounts.", file=discord.File(s, filename="players.txt")), bot.loop)
    asyncio.run_coroutine_threadsafe(channel.send(f"Data players last update <t:{awr}:R>"), bot.loop)

@bot.command()
async def showalt(ctx, rid = None, *, arg = None):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.author.id == 514394370804285460:
        True
      elif ctx.message.author.id == 746620014039138405:
        True
      elif ctx.message.author.id == 710537571276554283:
        True
      elif ctx.message.author.id == 420584968566079508:
        True
      elif ctx.message.author.id == 338130528538460160:
        True
      elif ctx.message.author.id == 792897995812765728:
        True
      elif ctx.message.author.id == 321507929289261057:
        True
      elif ctx.message.author.id == 611436125680041986:
        if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
          True
        else:
          return
      elif ctx.message.author.id == 616523087223062529:
        True
      elif ctx.message.author.id == 751857959625293995:
        if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
          True
        else:
          return
      elif ctx.message.author.id == 904800082480734209:
        if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
          True
        else:
          return
      # elif ctx.message.author.id == 976055468420108340: #HOPE
      #   if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
      #     True
      #   else:
      #     return
      elif ctx.message.author.id == 616035263692406796: #mrftank
        if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
          True
        else:
          return
      elif ctx.message.author.id == 913497847838703658: #Cyrio
        if ctx.message.channel.id == 1059112511967871036 or ctx.message.channel.id == 869619078820659210:
          True
        else:
          return
      else:
        return
      if rid is None:
        await ctx.send("Growid??")
        return
      ignorebanned = False
      if arg is not None:
        if "ignore" in arg:
            ignorebanned = True
            await ctx.send("Ignoring banned players")
      path = './players'
      aw = open("files/update.txt", "r")
      awr = aw.read()
      await ctx.send(f"Using ``new`` or ``old`` <t:{awr}:R> data?")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=15)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content.lower() == "new":
        try:
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': rid})
          if r.status_code == 200:
            True
          else:
            await ctx.send("New data is currently unavailable.")
          soup = BeautifulSoup(r.text, features='html.parser')
          values = [item.text.strip() for item in soup.select('.list')]
          if "Player was not found" in str(r.text):
            await ctx.send("Player is not exist.")
            return
          for ss in list(values):
            #print(ss)
            x = ss.split()
          if rid.lower() == "yuddy" or rid.lower() == "hiero":
            asd = os.path.exists(f"players\{rid}_.json")
            if asd == True:
              data2 = json.load(open(f"players\{rid}_.json", encoding='utf-8-sig'))
              playerip = data2["ip"]
              playermac = data2["mac"]
              if "rid" in data2:
                playerrid = data2["rid"]
          else:
            playerip = x[4]
            playermac = x[5]
            playerrid = x[8]
          asd = os.path.exists(f"players\{rid}_.json")
          if asd == True:
            data2 = json.load(open(f"players\{rid}_.json", encoding='utf-8-sig'))
            rawip = data2["ip"]
            rawmac = data2["mac"]
            if "rid" in data2:
              rawrid = data2["rid"]
            same = []
            different = []
            if playerip == rawip:
                same.append("IP")
            else:
                different.append("IP")
            if playermac == rawmac:
                same.append("MAC")
            else:
                different.append("MAC")
            if playerrid == rawrid:
                same.append("RID")
            else:
                different.append("RID")
            same_message = "Same : " + ", ".join(same) if same else "Same: None"
            different_message = "Different : " + ", ".join(different) if different else "Different: None"
            await ctx.send(f"{same_message}\n{different_message}\nCompared with <t:{awr}:R> data.")
        except:
           await ctx.send("Error")
           return
      elif msg.content.lower() == "old":
          asd = os.path.exists(f"players\{rid}_.json")
          if asd == True:
            data2 = json.load(open(f"players\{rid}_.json", encoding='utf-8-sig'))
            playerip = data2["ip"]
            playermac = data2["mac"]
            if "rid" in data2:
              playerrid = data2["rid"]
          else:
            await ctx.send("Cant find that growid in old data, try to use ``new`` data from panel.")
            aw = open("files/update.txt", "r")
            awr = aw.read()
            await ctx.send(f"Data players last update <t:{awr}:R>")
            return
      else:
           await ctx.send("Only ``new`` or ``old``.")
           return
      if playermac == "02:00:00:00:00:00":
        await ctx.send("Mac is 02:00:00:00:00:00, skipping mac.")
      await ctx.send(f"Showing matching ACCOUNT INFORMATION growid {rid}")
      threading.Thread(target=scanplayer, args=(rid, ctx.message.channel, ctx.message.author.id, playerip, playerrid, playermac)).start()
    #   start_time = time.time()
    #   wkwk, pop = scanplayer(playerip, playerrid, playermac)
    #   end_time = time.time()
    #   elapsed_time = end_time - start_time
    #   await ctx.send("Took {:.3f} seconds.".format(elapsed_time))
    #   aw = open("files/update.txt", "r")
    #   awr = aw.read()
    #   dones = (pop)
    #   dones = dones.replace("`6", "")
    #   dones = dones.replace("`0", "")
    #   dones = dones.replace("`9", "")
    #   dones = dones.replace("`", "")
    #   dones = dones.replace("**", "")
    #   s = StringIO()
    #   s.write(dones)
    #   s.seek(0)
    #   if len(pop) < 1999:
    #     await ctx.send(f"Found {wkwk} accounts.\n{dones}")
    #   else:
    #     await ctx.send(f"Found {wkwk} accounts.", file=discord.File(s, filename="players.txt"))
    #   await ctx.send(f"Data players last update <t:{awr}:R>")

@bot.command()
async def trackitemid(ctx, itemid):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.author.id == 514394370804285460:
        True
      elif ctx.message.author.id == 746620014039138405:
        True
      elif ctx.message.author.id == 825700430818443304:
        True
      elif ctx.message.author.id == 710537571276554283:
        True
      elif ctx.message.author.id == 420584968566079508:
        True
      elif ctx.message.author.id == 338130528538460160:
        True
      elif ctx.message.author.id == 792897995812765728:
        True
      elif ctx.message.author.id == 321507929289261057:
        True
      elif ctx.message.author.id == 616523087223062529:
        True
      else:
        return
      ignorebanned = False
      await ctx.send("Ignore banned players `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        await ctx.send('Ignoring banned players')
        ignorebanned = True
      elif msg.content == "y":
        await ctx.send('Ignoring banned players')
        ignorebanned = True
      else:
        await ctx.send("Ok")
        ignrebanned = False
      tt = 0
      path = './players'
      pop = ""
      dataid = json.load(open("files/itemsid.json", encoding='utf-8-sig'))
      wkwks = dataid["itemid"]
      nameitem = ""
      for data2id in dataid["itemid"]:
        dataid = data2id["id"]
        nameid = data2id["name"]
        testid = str(dataid)
        if testid == itemid:
            nameitem = nameid
            continue
      await ctx.send(f"Tracking itemid {itemid}({nameitem}) in backpack and inventory")
      total = 0
      for filename in glob.glob(os.path.join(path, '*_.json')):
        try:
          with open(filename, encoding='utf-8') as y:
          # wk = y.read()
            data = json.load(y)
            name = data["name"]
            level = data["level"]
            gems = data["gems"]
            rid = "no rid"
            mac = "no mac"
            banned = data["b_b"]
            reason = data["b_r"]
            long = data["b_s"]
            isbanned = banned
            isreason = reason
            islong = long
            gems = data["gems"]
            if banned == "":
              isbanned = "False"
            if isreason == "":
              isreason = "False"
            if long == "0":
              islong = "False"
            if "rid" in data:
              rid = data["rid"]
            if "mac" in data:
              mac = data["mac"]
            ip = data["ip"]
            if ignorebanned is True:
              if long == 0:
                True
              else:
                continue
            if "bp" in data:
             for bp in data["bp"]:
                gg = bp[0]
                if f"{itemid}" in str(gg):
                    amount = bp[1]
                    total = int(amount) + total
                    done = (f"[BACKPACK] Player {name} and level is {level} (has itemid {itemid} amount x{amount}) IP : {ip}, rid : {rid}, mac : {mac}, Banned : {isbanned}, Reason {reason}, how long {islong}, gems {gems}\n")
                    pop += done
                    tt = tt + 1
            if "inventory" in data:
             for inventory in data["inventory"]:
                gg = inventory[0]
                if f"{itemid}" in str(gg):
                    amount = inventory[1]
                    total = int(amount) + total
                    done = (f"[INVENTORY] Player {name} and level is {level} (has itemid {itemid} amount x{amount}) IP : {ip}, rid : {rid}, mac : {mac}, Banned : {isbanned}, Reason {reason}, how long {islong}, gems {gems}\n")
                    pop += done
                    tt = tt + 1
            if "inv" in data:
                for inv in data["inv"]:
                    amount = inv["c"]
                    itemiddata = inv["i"]
                    itemiddata = str(itemiddata)
                    #print(f"Item id is {itemid} and amount {item}")
                    if itemiddata == itemid:
                      total = amount + total
                     # print(filename)
                      done = (f"[OLD INVENTORY] Player {name} and level is {level} (has itemid {itemid} amount x{amount}) IP : {ip}, rid : {rid}, mac : {mac}, Banned : {isbanned}, Reason {reason}, how long {islong}, gems {gems}\n")
                      pop += done
                      tt = tt + 1
                      #print(f"[INVENTORY] Player {name} and level is {level} (has itemid {itemid} amount x{amount}) IP : {ip}, rid : {rid}, mac : {mac}, Banned : {isbanned}, Reason {reason}, how long {islong}\n")
        except:
          continue
      #kk = open("itemid players.txt", "a")
      #print(pop)
      #kk.write("test")
      #kk.write(pop)
      if pop == "":
        pop = "Empty"
      s = StringIO()
      s.write(pop)
      s.seek(0)
      #await ctx.send(file=discord.File(s, filename="test.txt"))
      if len(pop) < 1999:
        await ctx.send(f"Found {tt} players \n{pop}, total {total} items found")
      else:
        await ctx.send(f"Found {tt} players, total {total} items found", file=discord.File(s, filename="itemid players.txt"))
      aw = open("files/update.txt", "r")
      awr = aw.read()
      await ctx.send(f"Data players last update <t:{awr}:R>")

@bot.command()
async def getitemid(ctx, itemid):
  if ctx.message.author.id == 567561637951832083:
    True
  else:
    return
  data = json.load(open("files/itemsid.json", encoding='utf-8-sig'))
  wkwk = data["itemid"]
  for data2 in data["itemid"]:
    dataid = data2["id"]
    #print(dataid)
    name = data2["name"]
    test = str(dataid)
    if test == itemid:
        await ctx.send(f"Itemid **{itemid}** is **{name}**")
        return

@bot.command()
async def showinv(ctx, growid):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.author.id == 514394370804285460:
        True
      elif ctx.message.author.id == 746620014039138405:
        True
      elif ctx.message.author.id == 710537571276554283:
        True
      elif ctx.message.author.id == 420584968566079508:
        True
      elif ctx.message.author.id == 338130528538460160:
        True
      elif ctx.message.author.id == 792897995812765728:
        True
      elif ctx.message.author.id == 321507929289261057:
        True
      elif ctx.message.author.id == 611436125680041986:
        True
      elif ctx.message.author.id == 616523087223062529:
        True
      elif ctx.message.author.id == 751857959625293995:
        True
      elif ctx.message.author.id == 904800082480734209:
        True
      elif ctx.message.author.id == 976055468420108340: #HOPE
       True
      elif ctx.message.author.id == 616035263692406796: #mrftank
       True
      elif ctx.message.author.id == 913497847838703658: #Cyrio
       True
      else:
        return
      asd = os.path.exists(f"players\{growid}_.json")
      if asd == True:
        data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
      else:
        await ctx.send("Cant find that growid")
        aw = open("files/update.txt", "r")
        awr = aw.read()
        await ctx.send(f"Data players last update <t:{awr}:R>")
        return
      dataid = json.load(open("files/itemsid2.json", encoding='utf-8-sig'))
      tt = 0
      totalvalue = 0
      done = ""
      if "inv" in data:
        for inv in data["inv"]:
          amount = inv["c"]
          itemid = inv["i"]
          realid = str(itemid)
          if itemid == 0:
            continue
          try:
            nameitem = dataid[realid]
          except:
            nameitem = "None / Items Dat not updated"
          price = "Unkonwn"
          checkprice = os.path.exists(f"price\{realid}.json")
          if checkprice == True:
            dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
            price = dataprice["price"]
            pricereal = parse_price(price)
            if type(pricereal) == int:
                if "/" in price:
                   pricereal = amount / pricereal
                else:
                   pricereal = pricereal * amount
                totalvalue = pricereal + totalvalue
                pricereal = convert_to_locks(pricereal)
          done += (f"(Item Name : {nameitem}, ItemID : {itemid}, Amount : {amount}, Value {pricereal})\n")
        #  b = open("inventory.txt", "a")
         # b.write(f"{done}\n")
          tt = tt + 1
        s = StringIO()
        s.write(done)
        s.seek(0)
        totalvalue = convert_to_locks(totalvalue)
        if len(done) < 1999:
          await ctx.send(f"Found {tt} itemid, Total value : {totalvalue}.\n{done}")
        else:
          await ctx.send(f"Found {tt} itemid, Total value : {totalvalue}.", file=discord.File(s, filename="inventory.txt"))
      if "inventory" in data:
        for inventory in data["inventory"]:
          amount = inventory[1]
          itemid = inventory[0]
          realid = str(itemid)
          if itemid == 0:
            continue
          try:
            nameitem = dataid[realid]
          except:
            nameitem = "None / Items Dat not updated"
          pricereal = "Unkonwn"
          checkprice = os.path.exists(f"price\{realid}.json")
          if checkprice == True:
            dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
            price = dataprice["price"]
            pricereal = parse_price(price)
            if type(pricereal) == int:
                if "/" in price:
                   pricereal = amount / pricereal
                else:
                   pricereal = pricereal * amount
                totalvalue = pricereal + totalvalue
                pricereal = convert_to_locks(pricereal)
               # gg33 = convert_to_locks(totalvalue)
               # print(f"Name item : {nameitem}, Amount : {amount}, {pricereal}\nTotal Value : {gg33}")
          done += (f"(Item Name : {nameitem}, ItemID : {itemid}, Amount : {amount}, Value {pricereal})\n")
         # b = open("inventory.txt", "a")
         # b.write(f"{done}\n")
          tt = tt + 1
        #o = open("inventory.txt", "r")
       # da = o.read()
        s = StringIO()
        s.write(done)
        s.seek(0)
        totalvalue = convert_to_locks(totalvalue)
        if len(done) < 1999:
          await ctx.send(f"Found {tt} itemid, Total value : {totalvalue}.\n{done}")
        else:
          await ctx.send(f"Found {tt} itemid, Total value : {totalvalue}.", file=discord.File(s, filename="inventory.txt"))
      aw = open("files/update.txt", "r")
      awr = aw.read()
      await ctx.send(f"Data players last update <t:{awr}:R>")

@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def myvalue(ctx):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.guild.id == 1061469032408158218:
        True
      elif ctx.message.guild.id == 742792944079208540:
        if ctx.message.channel.id == 918522194798215239:
          True
        elif ctx.message.channel.id == 767108013752320020:
          True
        else:
          if discord.utils.get(ctx.message.author.roles, id=918543379590176818) is None:
            role = discord.utils.get(ctx.message.guild.roles, id=918543379590176818)
            await ctx.message.author.add_roles(role)
          await ctx.send("Please use this command in <#918522194798215239> channel only.")
          return
      elif ctx.message.guild.id == 771352967277182976:
        if ctx.message.channel.id == 1059112511967871036:
          True
        else:
          await ctx.send("This command can only be running in bot-command on GTPS3 Main Server.")
          return
      else:
        # await ctx.send("Not now")
        await ctx.send("This command can only be running in bot-command on GTPS3 Main Server.")
        return
      guild = bot.get_guild(771352967277182976)
      if guild.get_member(ctx.message.author.id) is not None:
        member = guild.get_member(ctx.message.author.id)
        growid = member.display_name
        asd = os.path.exists(f"players\{growid}_.json")
        if asd == True:
          data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
        else:
          await ctx.send(f"Your growid({growid}) is invalid.")
          aw = open("files/update.txt", "r")
          awr = aw.read()
          await ctx.send(f"This data is based on <t:{awr}:R> data.")
          return
        await ctx.send(f"<@{ctx.message.author.id}>, Would you like to **share** your inventory items to public? `yes`/`no`")
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel
        try:
          msg = await bot.wait_for("message", check=check, timeout=10)
        except asyncio.TimeoutError:
          await ctx.send("Canceled due to timer.")
          return
        if msg.content.lower() == "yes":
          dataid = json.load(open("files/itemsid2.json", encoding='utf-8-sig'))
          tt = 0
          totalvalue = 0
          totalvaluebp = 0
          totalitemsinbp = 0
          done = ""
          aw = open("files/update.txt", "r")
          awr = aw.read()
          awr = int(awr)
          time = unix_to_date(awr)
          if "inv" in data:
            awr = int(awr)
            time = unix_to_date(awr)
            done = f"╔═══════════════════════════════════════════════════════════════════════════════════════════\n╠INFORMATION : \n╠╡GrowID : {growid}\n╠╡Total items in inventory : lol wtf?\n╠╡Total inventory value : value of inventory\n╠╡Total items in backpack : totalnya items backpack\n╠╡Total backpack value : value backpack coy\n╠╡Total value : this is for all\n╠NOTES : \n╠╡You can suggest the unknown price by running command !suggestprice <Name item>.\n╠╡This inventory data is {time} data which mean if you wanna check your new value you have to wait until it updated.\n╠╡This command can only be running in bot-command on GTPS3 Main Server (https://discord.com/invite/gtps3).\n╠╡All prices provided here are based on the !checkprice command.\n╠╡You can also check other items by !checkprice with GTPS 3 Discord Bot.\n╠╡You can invite GTPS 3 Discord Bot with this link https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot.\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n"
            for inv in data["inv"]:
              amount = inv["c"]
              itemid = inv["i"]
              realid = str(itemid)
              if itemid == 0:
                continue
              try:
                nameitem = dataid[realid]
              except:
                nameitem = "None / Items Dat not updated"
              price = "Unkonwn"
              checkprice = os.path.exists(f"price\{realid}.json")
              if checkprice == True:
                try:
                  dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
                except:
                  continue
                price = dataprice["price"]
                by = dataprice["by"]
                pricereal = parse_price(price)
                if type(pricereal) == int:
                    if "/" in price:
                      pricereal = amount / pricereal
                    else:
                      pricereal = pricereal * amount
                    totalvalue = pricereal + totalvalue
                    pricereal = convert_to_locks(pricereal)
              if checkprice == True:
                done += (f"╠╡Item Name : {nameitem}\n╠╡Amount : {amount}\n╠╡Value : {pricereal} (price by {by})\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
              else:
                done += (f"╠╡Item Name : {nameitem}\n╠╡Amount : {amount}\n╠╡Value : {pricereal}\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
            #  b = open("inventory.txt", "a")
            # b.write(f"{done}\n")
              tt = tt + 1
            tt2 = str(tt)
            totalvalue = convert_to_locks(totalvalue)
            totalvalue2 = str(totalvalue)
            done = done.replace("lol wtf?", tt2)
            done = done.replace("what is wrong", totalvalue2)
            s = StringIO()
            s.write(done)
            s.seek(0)
            tt2 = str(tt)
          if "inventory" in data:
            awr = int(awr)
            time = unix_to_date(awr)
            done = f"╔═══════════════════════════════════════════════════════════════════════════════════════════\n╠INFORMATION : \n╠╡GrowID : {growid}\n╠╡Total items in inventory : lol wtf?\n╠╡Total inventory value : value of inventory\n╠╡Total items in backpack : totalnya items backpack\n╠╡Total backpack value : value backpack coy\n╠╡Total all items : this is all items\n╠╡Total value : this is for all\n╠NOTES : \n╠╡You can suggest the unknown price by running command !suggestprice <Name item>.\n╠╡This inventory data is {time} data which mean if you wanna check your new value you have to wait until it updated.\n╠╡This command can only be running in bot-command on GTPS3 Main Server (https://discord.com/invite/gtps3).\n╠╡All prices provided here are based on the !checkprice command.\n╠╡You can also check other items by !checkprice with GTPS 3 Discord Bot.\n╠╡You can invite GTPS 3 Discord Bot with this link https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot.\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n"
            for inventory in data["inventory"]:
              amount = inventory[1]
              itemid = inventory[0]
              realid = str(itemid)
              if itemid == 0:
                continue
              try:
                nameitem = dataid[realid]
              except:
                nameitem = "None / Items Dat not updated"
              pricereal = "Unkonwn"
              checkprice = os.path.exists(f"price\{realid}.json")
              if checkprice == True:
                try:
                  dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
                except:
                  continue
                price = dataprice["price"]
                by = dataprice["by"]
                pricereal = parse_price(price)
                if type(pricereal) == int:
                    if "/" in price:
                      pricereal = amount / pricereal
                    else:
                      pricereal = pricereal * amount
                    totalvalue = pricereal + totalvalue
                    pricereal = convert_to_locks(pricereal)
              if checkprice == True:
                done += (f"╠╡Item Name : {nameitem}\n╠╡Amount : {amount}\n╠╡Value : {pricereal} (price by {by})\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
              else:
                done += (f"╠╡Item Name : {nameitem}\n╠╡Amount : {amount}\n╠╡Value : {pricereal}\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
              tt = tt + 1
            tt2 = str(tt)
            totalvalueraw = totalvalue
            totalvalue = convert_to_locks(totalvalue)
            totalvalue2 = str(totalvalue)
            done = done.replace("lol wtf?", tt2)
            done = done.replace("value of inventory", totalvalue2)
         #   s = StringIO()
          #  s.write(done)
           # s.seek(0)
            tt2 = str(tt)
           # await ctx.send(f"Your growid is {growid}.\nFound **{tt}** items from your inventory.\nYour total value : **{totalvalue}**.\nThis inventory data is {time} data.", file=discord.File(s, filename="inventory.txt"))
          if "bp" in data:
            for bp in data["bp"]:
              amountbp = bp[1]
              itemidbp = bp[0]
             # print(amountbp)
             # print(itemidbp)
              realidbp = str(itemidbp)
              if itemidbp == 0:
                continue
              try:
                nameitembp = dataid[realidbp]
              except:
                nameitembp = "None / Items Dat not updated"
              pricerealbp = "Unkonwn"
              checkpricebp = os.path.exists(f"price\{realidbp}.json")
              if checkpricebp == True:
                try:
                  datapricebp = json.load(open(f"price\{realidbp}.json", encoding='utf-8-sig'))
                except:
                  continue
                pricebp = datapricebp["price"]
                bybp = datapricebp["by"]
                pricerealbp = parse_price(pricebp)
                if type(pricerealbp) == int:
                    if "/" in pricebp:
                      pricerealbp = amountbp / pricerealbp
                    else:
                      pricerealbp = pricerealbp * amountbp
                    totalvaluebp = pricerealbp + totalvaluebp
                    pricerealbp = convert_to_locks(pricerealbp)
              if checkpricebp == True:
                done += (f"╠╡Item Name : {nameitembp}\n╠╡Amount : {amountbp}\n╠╡Value : {pricerealbp} (price by {bybp})\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
              else:
                done += (f"╠╡Item Name : {nameitembp}\n╠╡Amount : {amountbp}\n╠╡Value : {pricerealbp}\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n")
              totalitemsinbp = totalitemsinbp + 1
            totalitemsinbp = str(totalitemsinbp)
            #print(totalvalue3)
            totalvaluebpraw = totalvaluebp
            totalvaluebp = convert_to_locks(totalvaluebp)
            totalvaluebp = str(totalvaluebp)
            done = done.replace("totalnya items backpack", totalitemsinbp)
            done = done.replace("value backpack coy", totalvaluebp)
            allitems = int(tt2) + int(totalitemsinbp)
            allitems = str(allitems)
            total = int(totalvalueraw) + int(totalvaluebpraw)
            done = done.replace("this is all items", allitems)
            totalgg = convert_to_locks(total)
            totalgg = str(totalgg)
            done = done.replace("this is for all", totalgg)
            s = StringIO()
            s.write(done)
            s.seek(0)
            # tt2 = str(tt2)
            await ctx.send(f"Your growid is **{growid}**.\nFound **{allitems}** items from your inventory and backpack.\nYour total value : **{totalgg}**.\nThis data is {time} data.", file=discord.File(s, filename="inventory.txt"))
        elif msg.content.lower() == "no":
          dataid = json.load(open("files/itemsid2.json", encoding='utf-8-sig'))
          tt = 0
          totalvalue = 0
          totalvaluebp = 0
          totalitemsinbp = 0
          done = ""
          aw = open("files/update.txt", "r")
          awr = aw.read()
          awr = int(awr)
          time = unix_to_date(awr)
          if "inv" in data:
            awr = int(awr)
            time = unix_to_date(awr)
            for inv in data["inv"]:
              amount = inv["c"]
              itemid = inv["i"]
              realid = str(itemid)
              if itemid == 0:
                continue
              try:
                nameitem = dataid[realid]
              except:
                nameitem = "None / Items Dat not updated"
              price = "Unkonwn"
              checkprice = os.path.exists(f"price\{realid}.json")
              if checkprice == True:
                try:
                  dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
                except:
                  continue
                price = dataprice["price"]
                by = dataprice["by"]
                pricereal = parse_price(price)
                if type(pricereal) == int:
                    if "/" in price:
                      pricereal = amount / pricereal
                    else:
                      pricereal = pricereal * amount
                    totalvalue = pricereal + totalvalue
                    pricereal = convert_to_locks(pricereal)
            #  b = open("inventory.txt", "a")
            # b.write(f"{done}\n")
              tt = tt + 1
            tt2 = str(tt)
            totalvalue = convert_to_locks(totalvalue)
            totalvalue2 = str(totalvalue)
          if "inventory" in data:
            awr = int(awr)
            time = unix_to_date(awr)
            done = f"╔═══════════════════════════════════════════════════════════════════════════════════════════\n╠INFORMATION : \n╠╡GrowID : {growid}\n╠╡Total items in inventory : lol wtf?\n╠╡Total inventory value : value of inventory\n╠╡Total items in backpack : totalnya items backpack\n╠╡Total backpack value : value backpack coy\n╠╡Total all items : this is all items\n╠╡Total value : this is for all\n╠NOTES : \n╠╡You can suggest the unknown price by running command !suggestprice <Name item>.\n╠╡This inventory data is {time} data which mean if you wanna check your new value you have to wait until it updated.\n╠╡This command can only be running in bot-command on GTPS3 Main Server (https://discord.com/invite/gtps3).\n╠╡All prices provided here are based on the !checkprice command.\n╠╡You can also check other items by !checkprice with GTPS 3 Discord Bot.\n╠╡You can invite GTPS 3 Discord Bot with this link https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot.\n╠═══════════════════════════════════════════════════════════════════════════════════════════\n"
            for inventory in data["inventory"]:
              amount = inventory[1]
              itemid = inventory[0]
              realid = str(itemid)
              if itemid == 0:
                continue
              try:
                nameitem = dataid[realid]
              except:
                nameitem = "None / Items Dat not updated"
              pricereal = "Unkonwn"
              checkprice = os.path.exists(f"price\{realid}.json")
              if checkprice == True:
                try:
                  dataprice = json.load(open(f"price\{realid}.json", encoding='utf-8-sig'))
                except:
                  continue
                price = dataprice["price"]
                by = dataprice["by"]
                pricereal = parse_price(price)
                if type(pricereal) == int:
                    if "/" in price:
                      pricereal = amount / pricereal
                    else:
                      pricereal = pricereal * amount
                    totalvalue = pricereal + totalvalue
                    pricereal = convert_to_locks(pricereal)
              tt = tt + 1
            tt2 = str(tt)
            totalvalueraw = totalvalue
            totalvalue = convert_to_locks(totalvalue)
            totalvalue2 = str(totalvalue)
         #   s = StringIO()
          #  s.write(done)
           # s.seek(0)
            tt2 = str(tt)
          if "bp" in data:
            for bp in data["bp"]:
              amountbp = bp[1]
              itemidbp = bp[0]
             # print(amountbp)
             # print(itemidbp)
              realidbp = str(itemidbp)
              if itemidbp == 0:
                continue
              try:
                nameitembp = dataid[realidbp]
              except:
                nameitembp = "None / Items Dat not updated"
              pricerealbp = "Unkonwn"
              checkpricebp = os.path.exists(f"price\{realidbp}.json")
              if checkpricebp == True:
                try:
                  datapricebp = json.load(open(f"price\{realidbp}.json", encoding='utf-8-sig'))
                except:
                  continue
                pricebp = datapricebp["price"]
                bybp = datapricebp["by"]
                pricerealbp = parse_price(pricebp)
                if type(pricerealbp) == int:
                    if "/" in pricebp:
                      pricerealbp = amountbp / pricerealbp
                    else:
                      pricerealbp = pricerealbp * amountbp
                    totalvaluebp = pricerealbp + totalvaluebp
                    pricerealbp = convert_to_locks(pricerealbp)
              totalitemsinbp = totalitemsinbp + 1
            totalitemsinbp = str(totalitemsinbp)
            #print(totalvalue3)
            totalvaluebpraw = totalvaluebp
            totalvaluebp = convert_to_locks(totalvaluebp)
            totalvaluebp = str(totalvaluebp)
            allitems = int(tt2) + int(totalitemsinbp)
            allitems = str(allitems)
            total = int(totalvalueraw) + int(totalvaluebpraw)
            totalgg = convert_to_locks(total)
            totalgg = str(totalgg)
            # tt2 = str(tt2)
            await ctx.send(f"Your GrowID : **{growid}**.\nTotal items in inventory : **{tt2}**.\nTotal inventory value :  **{totalvalue2}**.\nTotal items in backpack : **{totalitemsinbp}**.\nTotal backpack value : **{totalvaluebp}**.\nTotal all items : **{allitems}**.\nTotal value : **{totalgg}**.\nThis data is **{time}** data.")
        else:
          await ctx.send("Only `yes` or `no`.")
      else:
        await ctx.send("This command is restricted to moderators who are currently in the Mod Server.")
        return

@myvalue.error
async def myvalue_error(ctx, error):
    try:
        wkwk = round(error.retry_after)
    except:
        wkwk = 0
    await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.")


@bot.command()
async def showlastworld(ctx, growid):
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.author.id == 514394370804285460:
        True
      elif ctx.message.author.id == 746620014039138405:
        True
      elif ctx.message.author.id == 710537571276554283:
        True
      elif ctx.message.author.id == 420584968566079508:
        True
      elif ctx.message.author.id == 338130528538460160:
        True
      elif ctx.message.author.id == 792897995812765728:
        True
      elif ctx.message.author.id == 321507929289261057:
        True
      elif ctx.message.author.id == 611436125680041986:
        True
      elif ctx.message.author.id == 616523087223062529:
        True
      elif ctx.message.author.id == 751857959625293995:
        True
      elif ctx.message.author.id == 904800082480734209:
        True
      elif ctx.message.author.id == 976055468420108340: #HOPE
       True
      elif ctx.message.author.id == 616035263692406796: #mrftank
       True
      elif ctx.message.author.id == 913497847838703658: #Cyrio
       True
      else:
        return
      asd = os.path.exists(f"players\{growid}_.json")
      if asd == True:
        data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
      else:
        await ctx.send("Cant find that growid")
        aw = open("files/update.txt", "r")
        awr = aw.read()
        await ctx.send(f"Data players last update <t:{awr}:R>")
        return
      tt = 0
      done = ""
      if "la_wo" in data:
      #  a = open("last files/worlds.txt", "w")
        for world in data["la_wo"]:
          done += (f"Last worlds : {world}\n")
         # wkwk += done
          tt = tt + 1
        if done == "":
          await ctx.send("Empty")
          return
        if len(done) < 1999:
          await ctx.send(f"Found {tt} last worlds\n{done}")
        else:
          s = StringIO()
          s.write(done)
          s.seek(0)
          await ctx.send("Found {tt} last worlds", file=discord.File(s, filename="lastworld.txt"))
      else:
        await ctx.send("Doesn't have world")
      aw = open("files/update.txt", "r")
      awr = aw.read()
      await ctx.send(f"Data players last update <t:{awr}:R>")

@bot.command()
async def removegtpswl(ctx, growid = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      await ctx.send(f"Are you sure you want to remove **GTPS WLS** \"{growid}\"? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'gtpswl': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Removed GTPS WLS GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed GTPS WLS {growid}")
        return
      elif msg.content == "y":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'gtpswl': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Removed GTPS WLS GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} Removed GTPS WLS {growid}")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

@bot.command()
async def deleteaccount(ctx, growid = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      await ctx.send(f"Are you sure you want to **DELETE ACCOUNT** \"{growid}\"? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'delete_account': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Deleted account GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} DELETED ACOUNT {growid}")
        return
      elif msg.content == "y":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'delete_account': 1})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Deleted account GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} DELETED ACOUNT {growid}")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

@bot.command()
async def changepass(ctx, growid = None, *, newpass = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 751857959625293995: #cmol
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      if newpass is None:
       await ctx.send("enter the new password.")
       return
      await ctx.send(f"**Confirmation growid and new pass.**\nGrow ID : \"{growid}\"\nNew Pass : \"{newpass}\" \n`yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        if growid.lower() != "gamzz":
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'changepass': 1, 'last_name': newpass})
          if r.status_code == 200:
            True
          else:
            await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
            return
        await ctx.send(f"Changed password GrowID \"{growid}\", new password \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed pass {growid}, new pass {newpass}")
        return
      elif msg.content == "y":
        if growid.lower() != "gamzz":
          r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'changepass': 1, 'last_name': newpass})
          if r.status_code == 200:
            True
          else:
            await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
            return
        await ctx.send(f"Changed password GrowID \"{growid}\", new password \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed pass {growid}, new pass {newpass}")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return
 
@bot.command()
async def changeemail(ctx, growid = None, *, newpass = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      if newpass is None:
       await ctx.send("enter the new email.")
       return
      await ctx.send(f"**Confirmation GrowID and new email.**\nGrow ID : \"{growid}\"\nNew Email : \"{newpass}\" \n`yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'changeemail': 1, 'last_name': newpass})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Changed email growid \"{growid}\", new email \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed email {growid}, new email {newpass}")
        return
      elif msg.content == "y":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'changeemail': 1, 'last_name': newpass})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Changed email growid \"{growid}\", new email \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed email {growid}, new email {newpass}")
        return
      else:
        await ctx.send("Canceled.")
        return
      await ctx.send("Canceled due to timeout.")
      return
 
@bot.command()
async def change2fa(ctx, growid = None, *, newpass = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 751857959625293995: #cmol
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      if newpass is None:
       await ctx.send("enter the new 2fa.")
       return
      await ctx.send(f"**Confirmation GrowID and new 2fa.**\nGrow ID : \"{growid}\"\nNew 2fa : \"{newpass}\" \n`yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'change2fa': 1, 'last_name': newpass})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Changed 2fa growid \"{growid}\", new 2fa \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed 2fa {growid}, new 2fa {newpass}")
        return
      elif msg.content == "y":
        r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'change2fa': 1, 'last_name': newpass})
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Changed 2fa growid \"{growid}\", new 2fa \"{newpass}\".")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} changed 2fa {growid}, new 2fa {newpass}")
        return
      else:
        await ctx.send("Canceled.")
        return
      await ctx.send("Canceled due to timeout.")
      return

@bot.command()
async def checkdata(ctx, growid = None, *, newpass = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 746620014039138405: #vel
       True
      elif ctx.message.author.id == 710537571276554283: #key
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 751857959625293995: #cmol
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      if newpass is None:
       await ctx.send("enter the data you want to check.")
       return
      r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid})
      if r.status_code == 200:
        True
      else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
      soup = BeautifulSoup(r.text, features='html.parser')
      data = [item.text for item in soup.select('.list')]
      pp = str(data)
      if f"{newpass.lower()}" in pp.lower():
        await ctx.send(f"GrowID {growid}'s data contains {newpass}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} checked {growid}, data {newpass}")
        return
      else:
        await ctx.send(f"Unable to find {newpass} in {growid}'s data.")
        return

@bot.command()
async def givewls(ctx, growid = None, wls = None):
      if ctx.message.author.id == 567561637951832083: #cyrus
       True
      elif ctx.message.author.id == 420584968566079508: #gasky
       True
      elif ctx.message.author.id == 514394370804285460: #chris
       True
      elif ctx.message.author.id == 338130528538460160: #dndj
       True
      elif ctx.message.author.id == 616523087223062529: #devi
       True
      elif ctx.message.author.id == 710537571276554283:
       True
      else:
       return
      if growid is None:
       await ctx.send("enter the growid.")
       return
      if wls is None:
       await ctx.send("enter the wls amount.")
       return
      await ctx.send(f"Are you sure you want to give \"{growid}\" **{wls}** Premium WLS? `yes`/`no`")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=10)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      if msg.content == "yes":
        r = requests.post(f"http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/deposit.php?growid={growid}&deposit={wls}&rgt=")
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Sent **{wls}** Premium WLS to GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} gave {growid} {wls} Premium WLS")
        return
      elif msg.content == "y":
        r = requests.post(f"http://privategts1.eu/p3-=21p3=-123p21-=3/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/deposit.php?growid={growid}&deposit={wls}&rgt=")
        if r.status_code == 200:
         True
        else:
         await ctx.send(f"Website Down. <@{ctx.message.author.id}>")
         return
        await ctx.send(f"Sent **{wls}** Premium WLS to GrowID {growid}.")
        channel = bot.get_channel(983333089776390164)
        await channel.send(f"[LOGS] User {ctx.message.author} gave {growid} {wls} Premium WLS")
        return
      else:
        await ctx.send("Canceled")
        return
      await ctx.send("Canceled due to timeout")
      return

@bot.slash_command(name="test", description="GG!")
async def test(ctx): 
    await ctx.respond("lol gg")
 
@bot.slash_command(name="spin", description="lol you are retard!")
async def test(ctx): 
    await ctx.respond("gg you won")

@bot.command()
async def clown(ctx, user:discord.User = None):
  if ctx.message.author.id == 567561637951832083:
     True
  elif ctx.message.author.id == 420584968566079508:
     True
  else:
     return
  if user is None:
    await ctx.send("Please enter specific user.")
    return
  if not user.bot:
    if user.id == 567561637951832083:
      bot.clown = ctx.message.author.id
      await ctx.send(f"Clowned **yourself**")
    else:
      bot.clown = user
      await ctx.send(f"Clowned **{user.name}**")
  else:
    await ctx.send("You can\'t clown a bot")
    return

@bot.command()
async def stopclown(ctx):
  if ctx.message.author.id == 567561637951832083:
     True
  elif ctx.message.author.id == 420584968566079508:
     True
  else:
     return
  if bot.clown == None:
    await ctx.send("There was no one got clowned.")
    return
  else:
    await ctx.send(f"Stopped clown for **{bot.clown.name}**")
    bot.clown = None

@bot.command()
async def autodelete(ctx, user:discord.User = None):
  if ctx.message.author.id == 567561637951832083:
     True
  elif ctx.message.author.id == 420584968566079508:
     True
  else:
     return
  if user is None:
    await ctx.send("Please enter specific user.")
    return
  if not user.bot:
    if user.id == 567561637951832083:
      bot.autodelete = ctx.message.author.id
      await ctx.send(f"Autodeleting **yourself**")
    else:
      bot.autodelete = user
      await ctx.send(f"Auto deleting **{user.name}**")
  else:
    await ctx.send("You can\'t auto delete a bot")
    return

@bot.command()
async def stopautodelete(ctx):
  if ctx.message.author.id == 567561637951832083:
     True
  elif ctx.message.author.id == 420584968566079508:
     True
  else:
     return
  if bot.autodelete == None:
    await ctx.send("There was no one got auto deleted.")
    return
  else:
    await ctx.send(f"Stopped auto deleting for **{bot.clown.name}**")
    bot.autodelete = None

@bot.command()
async def backup(ctx):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    await ctx.send("Making backup")
    os.remove("backup.rar")
    patoolib.create_archive("backup.rar", ("verified/", "price/", "blacklist/", "blacklisted/", "files/itemsid.json", "files/itemsid2.json", "files/host.mp4", "files/list2.txt", "files/status.txt", "files/update.txt", "files/Virtual_Host.apk", "files/worlds.txt"));
    await ctx.send("Done")
    channel = bot.get_channel(983333006708191246)
    await channel.send(file=discord.File("backup.rar"))

@bot.command()
async def blacklistgrowid(ctx, *, growid = None):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    if growid == None:
      await ctx.send("Enter the growid")
      return
    aa = os.path.exists(f"blacklisted\{growid}.txt")
    if aa == True:
        await ctx.send("That growid is already in blacklist")
        return
    ee = open(f"blacklisted\{growid}.txt", "w")
    await ctx.send("Done")

@bot.command()
async def checkmod(ctx, user:discord.Member):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    hasmod = False
    name = user.display_name
    bb = os.path.exists(f"players\{name}_.json")
    if bb == True:
      data = json.load(open(f"players\{name}_.json", encoding='utf-8-sig'))
      for playmods in data["playmods"]:
        idmod = playmods["id"]
        timer = playmods["time"]
        if idmod == 125:
         await ctx.send("Has mod")
         hasmod = True
         break
      if hasmod == False:
        await ctx.send(f"Growid {name}, user {user}({user.id}) doesn't have mod consumable.\n")
    else:
      await ctx.send(f"{name} is not exist in database")

@bot.command()
async def scanmods(ctx):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    a = 0
    listname = ""
    listname2 = ""
    listname3 = ""
    for i in ctx.guild.members:
     a = a + 1
    await ctx.send(f"Scanning {a} members.")
    total = 0
    total2 = 0
    total3 = 0
    for user in ctx.guild.members:
      hasmod = False
      if user.bot:
        continue
      if str(user.top_role) != "Mod":
        continue
      name = user.display_name
      bb = os.path.exists(f"players\{name}_.json")
      if bb == True:
        data = json.load(open(f"players\{name}_.json", encoding='utf-8-sig'))
        banned = data["b_b"]
        reason = data["b_r"]
        long = data["b_s"]
        if "mod2" in data:
          mod = data["mod2"]
          if mod == 1:
            hasmod = True
        if banned == "":
          True
        else:
          done = (f"Growid {name}, user {user}({user.id}) is banned by {banned} reason {reason} for {long}.\n")
          total = total + 1
          listname += done
          continue
        for playmods in data["playmods"]:
          idmod = playmods["id"]
          timer = playmods["time"]
          if idmod == 125:
           hasmod = True
           break
        if hasmod == False:
          done2 = (f"Growid {name}, user {user}({user.id}) doesn't have mod consumable.\n")
          total2 = total2 + 1
          listname2 += done2
          continue
      else:
        done3 = (f"Growid {name}, user {user}({user.id}) is not exist in player database.\n")
        total3 = total3 + 1
        listname3 += done3
        continue
    s = StringIO()
    s.write(listname3)
    s.seek(0)
    await ctx.send(f"Total not exists account **{total3}**.", file=discord.File(s, filename="Not_Exists.txt"))
    s = StringIO()
    s.write(listname)
    s.seek(0)
    await ctx.send(f"Total banned mods **{total}**.", file=discord.File(s, filename="Banned_Mods.txt"))
    s = StringIO()
    s.write(listname2)
    s.seek(0)
    await ctx.send(f"Total mods doesnt have mod consumable **{total2}**.", file=discord.File(s, filename="No_Mod_Consumable.txt"))
  #  print(total)

@bot.command()
async def kickmods(ctx):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    a = 0
    channel = bot.get_channel(869619078820659210)
    listname = ""
    listname2 = ""
    listname3 = ""
    for i in ctx.guild.members:
     a = a + 1
    await ctx.send(f"Scanning and kicking **{a}** users.")
    total = 0
    total2 = 0
    total3 = 0
    guild = bot.get_guild(771352967277182976)
    for user in ctx.guild.members:
      hasmod = False
      if user.bot:
        continue
      if str(user.top_role) != "Mod":
        continue
      name = user.display_name
      bb = os.path.exists(f"players\{name}_.json")
      if bb == True:
        data = json.load(open(f"players\{name}_.json", encoding='utf-8-sig'))
        banned = data["b_b"]
        reason = data["b_r"]
        long = data["b_s"]
        if "mod2" in data:
          mod = data["mod2"]
          if mod == 1:
            hasmod = True
        if banned == "":
          True
        else:
          done = (f"Kicked {user}({user.id}), GrowID {name} Player is banned.\n")
          total = total + 1
          listname += done
          try:
            await guild.kick(user, reason="Player is banned in-game.")
            print(done)
          except:
            await channel.send(f"Unable to kick {user} (player is banned).")
            print(f"Unable to kick {user} (player is banned).")
          continue
        for playmods in data["playmods"]:
          idmod = playmods["id"]
          timer = playmods["time"]
          if idmod == 125:
           hasmod = True
           break
        if hasmod == False:
          done2 = (f"Kicked {user}({user.id}), GrowID {name} doesn't have mod consumable in-game.\n")
          total2 = total2 + 1
          listname2 += done2
          ww = os.path.exists(f"verified\{user.id}_.txt")
          if ww == True:
            os.remove(f"verified\{user.id}_.txt")
            done4 = (f"{user.name}'s verify has been reseted.\n")
            listname2 += done4
          ww = os.path.exists(f"verified\{name}_.txt")
          if ww == True:
            os.remove(f"verified\{name}_.txt")
            done5 = (f"{name}'s verify has been reseted.\n")
            listname2 += done5
          try:
            await user.send("You have been kicked from **Mod Server GTPS3** for not having mod role in-game.")
          except:
            pass
          try:
            await guild.kick(user, reason="Player doesn't have mod consumable.")
            print(done2)
          except:
            await channel.send(f"Unable to kick {user} (no mod consumable).")
            print(f"Unable to kick {user} (no mod consumable).")
          continue
      else:
        done3 = (f"Kicked {user}({user.id}), GrowID {name} is not exist in database.\n")
        total3 = total3 + 1
        listname3 += done3
        ww = os.path.exists(f"verified\{user.id}_.txt")
        if ww == True:
          os.remove(f"verified\{user.id}_.txt")
          done4 = (f"{user}'s verify has been reseted.\n")
          listname2 += done4
        ww = os.path.exists(f"verified\{name}_.txt")
        if ww == True:
          os.remove(f"verified\{name}_.txt")
          done5 = (f"{name}'s verify has been reseted.\n")
          listname2 += done5
        try:
          await user.send("You have been kicked from **Mod Server GTPS3** your GrowID is not exists in database.")
        except:
          pass
        try:
          await guild.kick(user, reason="Player not exists in database.")
          print(done3)
        except:
          await channel.send(f"Unable to kick {user} (not exists in database).")
          print(f"Unable to kick {user} (not exists in database).")
        continue
    s = StringIO()
    s.write(listname3)
    s.seek(0)
    await channel.send(f"Total kicked not exists account **{total3}**.", file=discord.File(s, filename="Kicked_Not_Exists.txt"))
    s = StringIO()
    s.write(listname)
    s.seek(0)
    await channel.send(f"Total kicked banned mods **{total}**.", file=discord.File(s, filename="Kicked_Banned_Mods.txt"))
    s = StringIO()
    s.write(listname2)
    s.seek(0)
    await channel.send(f"Total kicked mods doesnt have mod consumable **{total2}**.", file=discord.File(s, filename="Kicked_No_Mod_Consumable.txt"))
    count = total+total2+total3
    b = a-count
    await ctx.send(f"**{count}** Users have been kicked from GTPS3 Mod Server.\n- Total users don't have mod role in game : **{total2}**\n- Total users don't exists in database : **{total3}**\n- Total users banned in-game : **{total}**\nGTPS3 - MODS Server member count **{a}** -> **{b}**.")


@bot.command()
async def updateprice(ctx, itemid = None, *, price = None):
   # role = discord.utils.find(lambda r: r.id == 744347026635882616, ctx.message.guild.roles)
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 321507929289261057:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    elif ctx.message.author.id == 746620014039138405:
      True
    elif ctx.message.author.id == 710537571276554283:
      True
    elif ctx.message.author.id == 420584968566079508:
      True
    elif ctx.message.author.id == 338130528538460160:
      True
    elif ctx.message.author.id == 792897995812765728:
      True
    elif ctx.message.author.id == 321507929289261057:
      True
    elif ctx.message.author.id == 611436125680041986:
      True
    elif ctx.message.author.id == 616523087223062529:
      True
    elif ctx.message.author.id == 751857959625293995:
      True
    elif ctx.message.channel.id == 767108013752320020:
      True
    else:
      return
    if itemid == None:
      await ctx.send("Enter the itemid. ``ex : !updateprice 7188 20-100 Diamond Locks``")
      return
    if price == None:
      await ctx.send("Enter the price. ``ex : !updateprice 7188 20-100 Diamond Locks``")
      return
    e = "{"
    w = "}"
    itemname = ""
    oooo = is_utf8(ctx.message.author)
    if oooo == True:
      by = ctx.message.author
    else:
      by = ctx.message.author.id
    dataid = json.load(open("files/itemsid.json", encoding='utf-8-sig'))
    if price.lower() == "wl" or price.lower() == "dl" or price.lower() == "bgl":
      price = price.lower()
      price = price.replace("wl", "World Lock")
      price = price.replace("dl", "Diamond Lock")
      price = price.replace("bgl", "Blue Gem Lock")
    for data2id in dataid["itemid"]:
      dataid = data2id["id"]
      nameid = data2id["name"]
      testid = str(dataid)
      if testid == itemid:
          itemname = nameid
          continue
    if itemname == "":
      await ctx.send("Unable to find that item")
      return
    aa = os.path.exists(f"price\{itemid}.json")
    if aa == True:
       try:
        data = json.load(open(f"price\{itemid}.json", encoding='utf-8-sig'))
       except:
         await ctx.send("Error")
         return
       price2 = data["price"]
       update3 = data["last"]
       name2 = data["name"]
       by3 = data["by"]
       by2 = f"**{by3}**"
       update2 = f"<t:{update3}:R>"
    else:
       price2 = "-"
       update2 = "**-**"
       name2 = "-"
       by2 = "**-**"
    ee = open(f"price\{itemid}.json", "w")
    time = str(round(datetime.datetime.now().timestamp()))
    try:
      ee.write(f"{e}\"price\":\"{price}\", \"name\":\"{itemname}\", \"by\":\"{by}\", \"last\":\"{time}\"{w}")
    except:
      by = ctx.message.author.id
      ee.write(f"{e}\"price\":\"{price}\", \"name\":\"{itemname}\", \"by\":\"{by}\", \"last\":\"{time}\"{w}")
    embed=discord.Embed(title=f"Updated {itemname}'s price", description=f'**Old Price**\n♦️ Name Item : **{name2}**\n♦️ Price Item : **{price2}**\n♦️ Last Update Price : {update2} by {by2}\n\n**New Price**\n🔹 Name Item : **{itemname}**\n🔹 Price Item : **{price}**\n🔹 Last Update Price : <t:{time}:R> by **{ctx.message.author}**', color=0x00FF00)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)
    channel = bot.get_channel(983333089776390164)
    await channel.send(embed=embed)
    #await ctx.send(f"Updated price ItemID **{itemid}**, Name item **{itemname}** for **{price}**.")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def checkprice(ctx, *, itemname = None):
    if ctx.message.guild.id == 742792944079208540:
      if ctx.message.channel.id == 767108013752320020:
        True
      elif ctx.message.channel.id == 918522194798215239:
        True
      elif ctx.message.channel.id == 995716819044286504:
        True
      elif ctx.message.channel.id == 977619932042907718:
        True
      else:
        if discord.utils.get(ctx.message.author.roles, id=918543379590176818) is None:
          role = discord.utils.get(ctx.message.guild.roles, id=918543379590176818)
          await ctx.message.author.add_roles(role)
        await ctx.send("Please use this command in <#918522194798215239> channel only.")
        return
    if ctx.message.guild.id == 771352967277182976:
      if ctx.message.author.id == 567561637951832083:
        True
      elif ctx.message.channel.id == 1059112511967871036:
        True
      else:
        return
    #elif ctx.message.channel.id == 983333074181951498:
      #True
    #else:
      #await ctx.send("Use this command in <#980102052791349268>!")
      #return
    if itemname == None:
      await ctx.send("Enter the item name.")
      return
    if len(itemname) < 3:
      await ctx.send("Please enter atleast 3 letters.")
      return
    found = False
    found2 = False
    path = './price'
    matching_items = []
    realname = itemname.lower()
    for filename in glob.glob(os.path.join(path, '*.json')):
     try:
        data = json.load(open(filename, encoding='utf-8-sig'))
        price = data["price"]
        update = data["last"]
        name = data["name"]
        name2 = str(name)
        by = data["by"]
        if f"{realname}" in name2.lower():
         if found != True:
            embed=discord.Embed(title=f"Price for {name}", description=f'🔹 Name Item : **{name}**\n🔹 Price Item : **{price}**\n🔹 Last Update Price : <t:{update}:R> by **{by}**', color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
            found = True
            #await ctx.send(f"Name item **{name}**, price is **{price}**, last update price <t:{update}:R> by {by}.")
        if realname == name2.lower():
            embed=discord.Embed(title=f"Price for {name}", description=f'🔹 Name Item : **{name}**\n🔹 Price Item : **{price}**\n🔹 Last Update Price : <t:{update}:R> by **{by}**', color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.message.author}")
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
            await ctx.send(embed=embed)
            return
        if fuzz.partial_ratio(realname, name2.lower()) > 70:
            matching_items.append(f"**{name2}**")
     except:
        print(f"Error in {filename}")
        continue
    if found == True:
        await ctx.send(embed=embed)
        return
    if len(matching_items) > 0:
      embed=discord.Embed(description=f"Unable to find item with name **{itemname}**.\nDid you mean : {', '.join(matching_items)}?\n\nStill unable to find item you looking for in above? you can suggest it to our bot.\n**!suggestprice <Name Item>**\n╰▸ ex : **!suggestprice Legendary Cyrus's katana**", color=0xFF0000)
    else:
      embed=discord.Embed(description=f"Unable to find item with name **{itemname}**\n\nYou can simply suggest the item that you looking for to our bot.\n**!suggestprice <Name Item>**\n╰▸ ex : **!suggestprice Legendary Cyrus's katana**\nNote : Not all items are gonna be added to the bot.", color=0xFF0000)
    embed.set_footer(text=f"Try to enter exact same item name or similar item name | Requested by {ctx.message.author}")
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def suggestprice(ctx, *, name = None):
      if ctx.message.guild.id == 742792944079208540:
        if ctx.message.channel.id == 767108013752320020:
          True
        elif ctx.message.channel.id == 918522194798215239:
          True
        elif ctx.message.channel.id == 995716819044286504:
          True
        elif ctx.message.channel.id == 977619932042907718:
          True
        else:
          await ctx.send("Please use this command in bot commands channel only.")
          return
      else:
        await ctx.send("This command can only be running in bot-command on GTPS3 Main Server.\nJoin us https://discord.com/invite/gtps3")
        return
      if name is None:
        await ctx.send("Please enter the item name.")
        return
      name = name.replace("@", "@ ")
      await ctx.send(f"What is the price for **{name}**?\nif you don't know the price yet just write \"-\".")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=20)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time.")
        return
      price = msg.content
      if price == "-":
         price = "User doesn't know the price."
      embed=discord.Embed(title="Price Suggestion", description=f'🔸 Name Item : **{name}**\n🔸 Price Item : **{price}**', color=discord.Colour.random())
      embed.set_footer(text=f"Requested by {ctx.message.author}")
      await ctx.send("Thank you for your suggestion. We appreciate your input and our support team will take your suggestion into consideration.")
      channel = bot.get_channel(767108013752320020)
      await channel.send(f"Suggestion by {ctx.message.author}({ctx.message.author.id})", embed=embed)

@suggestprice.error
async def suggestprice_error(ctx, error):
    try:
        wkwk = round(error.retry_after)
    except:
        wkwk = 0
    await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.")


@checkprice.error
async def checkprice_error(ctx, error):
    try:
        wkwk = round(error.retry_after)
    except:
        wkwk = 0
    await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.")

@bot.command()
async def resetprice(ctx, itemid = None):
    #role = discord.utils.find(lambda r: r.id == 744347026635882616, ctx.message.guild.roles)
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 321507929289261057:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    elif ctx.message.author.id == 746620014039138405:
      True
    elif ctx.message.author.id == 710537571276554283:
      True
    elif ctx.message.author.id == 420584968566079508:
      True
    elif ctx.message.author.id == 338130528538460160:
      True
    elif ctx.message.author.id == 792897995812765728:
      True
    elif ctx.message.author.id == 321507929289261057:
      True
    elif ctx.message.author.id == 611436125680041986:
      True
    elif ctx.message.author.id == 616523087223062529:
      True
    elif ctx.message.author.id == 751857959625293995:
      True
    elif ctx.message.channel.id == 767108013752320020:
      True
    else:
      return
    if itemid == None:
      await ctx.send("Enter the itemid")
      return
    aa = os.path.exists(f"price\{itemid}.json")
    dataid = json.load(open("files/itemsid2.json", encoding='utf-8-sig'))
    names = "None"
    try:
      names = dataid[itemid]
    except:
      names = "None"
    if aa == True:
       data = json.load(open(f"price\{itemid}.json", encoding='utf-8-sig'))
       price2 = data["price"]
       update3 = data["last"]
       name2 = data["name"]
       by3 = data["by"]
       by2 = f"**{by3}**"
       update2 = f"<t:{update3}:R>"
    else:
       await ctx.send(f"{names}'s itemid is not exist in price database yet.")
       return
    os.remove(f"price\{itemid}.json")
    await ctx.send(f"Reseted {names}'s itemid({itemid}) price.")
    log = bot.get_channel(983333089776390164)
    await log.send(f"[LOGS] User {ctx.message.author} reseted {itemid} price\n♦️ Name Item : **{name2}**\n♦️ Price Item : **{price2}**\n♦️ Last Update Price : {update2} by {by2}")

@bot.command()
async def findid(ctx, *, nameitem):
  data = json.load(open("files/itemsid.json", encoding='utf-8-sig'))
  nameitem2 = nameitem.lower()
  listname = ""
  tt = 0
  if ctx.message.author.id == 491651928720408586:
    return
  if ctx.message.author.id == 567561637951832083:
    True
  elif ctx.message.channel.id == 767108013752320020:
    True
  elif ctx.message.channel.id == 742806328652595291:
    True
  elif ctx.message.channel.id == 742806328652595291:
    True
  else:
    return
  if len(nameitem) < 3:
    await ctx.send("Please enter atleast 3 letters.")
    return
  for data2 in data["itemid"]:
    dataid = data2["id"]
    name = data2["name"]
    name2 = str(name)
    if f"{nameitem2}" in name2.lower():
        tt = tt + 1
        done = (f"Found itemid **{dataid}**, **{name}**\n")
        listname += done
  if len(listname) < 1999:
        await ctx.send(f"Total items found **{tt}**,\n{listname}")
  else:
        listname = listname.replace("**", "")
        s = StringIO()
        s.write(listname)
        s.seek(0)
        await ctx.send(f"Total items found **{tt}**", file=discord.File(s, filename="id items.txt"))

@bot.command()
async def blacklistuser(ctx, user:discord.User = None):
  if ctx.message.author.id == 567561637951832083:
      True
  elif ctx.message.author.id == 514394370804285460:
      True
  else:
      return
  if user is None:
    await ctx.send("Please enter the user.")
    return
  aa = os.path.exists(f"blacklisted\{ctx.message.author.id}.txt")
  if aa == True:
    await ctx.send("That user is already in blacklist")
    return
  ee = open(f"blacklisted\{user.id}.txt", "w")
  await ctx.send("Done")

@bot.command()
async def resetblacklistgrowid(ctx, *, growid = None):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 514394370804285460:
      True
    else:
      return
    if growid == None:
      await ctx.send("Enter the growid")
      return
    aa = os.path.exists(f"blacklisted\{growid}.txt")
    if aa == False:
        await ctx.send("That growid is not in blacklist")
        return
    os.remove(f"blacklisted\{growid}.txt")
    await ctx.send("Done")

@bot.command()
async def resetblacklistuser(ctx, user:discord.User = None):
  if ctx.message.author.id == 567561637951832083:
      True
  elif ctx.message.author.id == 514394370804285460:
      True
  else:
      return
  if user is None:
    await ctx.send("Please enter the user.")
    return
  aa = os.path.exists(f"blacklisted\{ctx.message.author.id}.txt")
  if aa == False:
    await ctx.send("That user is not in blacklist")
    return
  os.remove(f"blacklisted\{user.id}.txt")
  await ctx.send("Done")

@bot.command()
@commands.dm_only()
@commands.cooldown(1, 30, commands.BucketType.user)
async def verify(ctx, growid = None, *, email = None):
 #   if ctx.message.author.id == 536221832668381195:
 #     True 
 #   else:
  #    await ctx.send("Mod server is currently closed, check again in few minutes.")
   #   return
    hasmod = False
    guild = bot.get_guild(771352967277182976)
    if guild.get_member(ctx.message.author.id) is not None:
      await ctx.send("You are already in Ps Mod. You don't have to.")
      return
    aa = os.path.exists(f"blacklist\{ctx.message.author.id}.txt")
    if aa == True:
      with open(f"blacklist\{ctx.message.author.id}.txt", "r") as j:
        wk = j.read()
        if wk == "4":
          await ctx.send("You are currently blacklisted. To appeal this reach our support in support channel.")
          return
    if growid is None:
      await ctx.send("Plase enter the growid.\nUsage : `!recovery <GrowID> <Email>`.")
      return
    if email is None:
      await ctx.send("Plase enter the email.\nUsage : `!recovery <GrowID> <Email>`.")
      return
    try:
      data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
    except FileNotFoundError:
      #await ctx.send("Mod server is currently closed, check again later.")
      await ctx.send("That user is not allowed.")
      return
    emaildata = data["email"]
    ban = data["b_s"]
    mod = data["mod2"]
    realname = data["name"]
    kk = os.path.exists(f"verified\{ctx.message.author.id}_.txt")
    if kk == True:
      yy = open(f"verified\{ctx.message.author.id}_.txt", "r")
      oo = yy.read()
      await ctx.send(f"You are already verified with GrowID \"{oo}\".")
      return
    if ban == 0:
      True
    else:
      await ctx.send("That user is not allowed.")
    oooo = is_utf8(ctx.message.author)
    if oooo == True:
      lolz = f"{ctx.message.author} ({ctx.message.author.id})"
    else:
      lolz = f"({ctx.message.author.id})"
    times = "0"
    for playmods in data["playmods"]:
      idmod = playmods["id"]
      if idmod == 125:
       hasmod = True
       break
    if hasmod == False:
      if mod == 1:
        True
      else:
        await ctx.send("That user is not allowed. (if you believe you had mod role ingame wait until bot's database updated)")
        return
    ll = os.path.exists(f"blacklisted\{ctx.message.author.id}.txt")
    if ll == True:
      await ctx.send("That user is not allowed.")
      return
    uu = os.path.exists(f"blacklisted\{growid}.txt")
    if uu == True:
      await ctx.send("That user is not allowed.")
      return
    if email.lower() == emaildata.lower():
      aq = os.path.exists(f"verified\{growid}_.txt")
      if aq == True:
        ii = open(f"verified\{growid}_.txt", "r")
        gg = ii.read()
        await ctx.send(f"{growid} is already verified by {gg}.")
        return
    else:
      dataemail = getdata(growid)
      emaildata = dataemail['email']
      if email.lower() == emaildata.lower():
        await ctx.send("That user is not allowed. (if you believe you had mod role ingame wait until bot's database updated)")
        return
      if aa == False:
        f = open(f"blacklist\{ctx.message.author.id}.txt", "w")
        f.write("1")
      else:
        with open(f"blacklist\{ctx.message.author.id}.txt", "r") as o:
          qq = o.read()
          oo = 1
          if qq == "1":
            f = open(f"blacklist\{ctx.message.author.id}.txt", "w")
            f.write("2")
            oo = 2
          elif qq == "2":
            f = open(f"blacklist\{ctx.message.author.id}.txt", "w")
            f.write("3")
            oo = 3
          elif qq == "3":
            f = open(f"blacklist\{ctx.message.author.id}.txt", "w")
            f.write("4")
            oo = 4
          channel = bot.get_channel(974256030454272001)
          embed=discord.Embed(description="**Wrong Email Logs**", color=0xFF0000)
          embed.set_author(name=ctx.message.author)
          embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=True)
          embed.add_field(name="Growid", value=realname, inline=True)
          embed.add_field(name="Email", value=email, inline=True)
          embed.add_field(name="Real Email", value=emaildata, inline=True)
          embed.set_footer(text=f"ID : {ctx.message.author.id} | Attempt {oo}/4")
          await ctx.send(f"Please enter exact same email. ({oo}/4)")
          await channel.send(embed=embed)
          return
      channel = bot.get_channel(974256030454272001)
      embed=discord.Embed(description="**Wrong Email Logs**", color=0xFF0000)
      embed.set_author(name=ctx.message.author)
      embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Growid", value=realname, inline=True)
      embed.add_field(name="Email", value=email, inline=True)
      embed.add_field(name="Real Email", value=emaildata, inline=True)
      embed.set_footer(text=f"ID : {ctx.message.author.id} | Attempt 1/4")
      await channel.send(embed=embed)
      await ctx.send("Please enter exact same email. (1/4)")
      return
    channel = bot.get_channel(771352967277182984)
    ee = open(f"verified\{ctx.message.author.id}_.txt", "w")
    ee.write(realname)
    link = await channel.create_invite(max_age = 600, max_uses = 1)
    channel = bot.get_channel(974256030454272001)
    await ctx.send(f"You are Verified.\nThis link will expire in 10 minutes. {link}")
    embed=discord.Embed(description="**Verified Logs**", color=0x32CD32)
    embed.set_author(name=ctx.message.author)
    embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=True)
    embed.add_field(name="Growid", value=realname, inline=True)
    embed.add_field(name="Email", value=email, inline=True)
    embed.add_field(name="Invite Link", value=link, inline=True)
    embed.set_footer(text=f"ID : {ctx.message.author.id}")
    await channel.send(embed=embed)
    dd = open(f'verified\{realname}_.txt', 'w')
    try:
      dd.write(lolz)
    except:
      dd.write(lolz)
    
@bot.command()
@commands.dm_only()
@commands.cooldown(1, 30, commands.BucketType.user)
async def verifi(ctx, growid = None, *, email = None):
  await ctx.send("Pemanent mods now able to use ``!verify``")
  return

@bot.command()
async def whyuserisnotallowed(ctx, growid = None, user:discord.User = None):
    role = discord.utils.find(lambda r: r.id == 997128751563411486, ctx.message.guild.roles)
    if ctx.message.author.id == 567561637951832083:
        True
    elif role in ctx.message.author.roles:
        True
    else:
        await ctx.send("Banning yourself from server in few seconds.")
        return
    if growid is None:
        await ctx.send("Growid ??")
        return
    if user is None:
        await ctx.send("User ??")
        return
    try:
        data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
    except FileNotFoundError:
        #await ctx.send("Mod server is currently closed, check again later.")
        await ctx.send("Account not exist")
        return
    ll = os.path.exists(f"blacklisted\{user.id}.txt")
    if ll == True:
        await ctx.send("User blacklisted")
        return
    uu = os.path.exists(f"blacklisted\{growid}.txt")
    if uu == True:
        await ctx.send("Growid blacklisted")
        return
    ban = data["b_s"]
    banned = data["b_b"]
    reason = data["b_r"]
    if ban == 0:
        True
    else:
        await ctx.send(f"Growid is banned by {banned} for {reason}")
        return
    await ctx.send("??? unkown tell dev most likely the user is allowed")

@bot.command()
async def manualverify(ctx, growid = None, user:discord.User = None):
    role = discord.utils.find(lambda r: r.id == 997128751563411486, ctx.message.guild.roles)
    if ctx.message.author.id == 567561637951832083:
        True
    elif role in ctx.message.author.roles:
        True
    else:
        await ctx.send("Banning yourself from server in few seconds.")
        return
    if growid is None:
        await ctx.send("Growid ??")
        return
    if user is None:
        await ctx.send("User ??")
        return
    try:
        data = json.load(open(f"players\{growid}_.json", encoding='utf-8-sig'))
    except FileNotFoundError:
        #await ctx.send("Mod server is currently closed, check again later.")
        await ctx.send("Growid not exist")
    ll = os.path.exists(f"blacklisted\{user.id}.txt")
    if ll == True:
        await ctx.send("User manually blacklisted")
        return
    uu = os.path.exists(f"blacklisted\{growid}.txt")
    if uu == True:
        await ctx.send("Growid manually blacklisted")
        return
    ban = data["b_s"]
    banned = data["b_b"]
    reason = data["b_r"]
    if ban == 0:
        True
    else:
        await ctx.send(f"Growid is banned by {banned} for {reason}")
    ee = open(f"verified\{user.id}_.txt", "w")
    ee.write(growid)
    channel = bot.get_channel(771352967277182984)
    link = await channel.create_invite(max_age = 600, max_uses = 1)
    await user.send(f"You are Manually Verified to GTPS3 Mod Server.\nThis link will expire in 10 minutes. {link}")
    await ctx.send(f"Manually Verified GrowID {growid}, User {user} and sent Mod server invite.")
    dd = open(f'verified\{growid}_.txt', 'w')
    try:
      dd.write(f"{user} ({user.id})")
    except:
      dd.write(f"{user.id}")
    channel = bot.get_channel(974256030454272001)
    embed=discord.Embed(description="**Manual Verified Logs**", color=0x32CD32)
    embed.set_author(name=f"Verified {user} by {ctx.message.author}")
    embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
    embed.add_field(name="Growid", value=growid, inline=True)
    embed.add_field(name="Invite Link", value=link, inline=True)
    embed.set_footer(text=f"ID : {user.id}")
    await channel.send(embed=embed)

@bot.command()
async def whoban(ctx, growid = None):
    role = discord.utils.find(lambda r: r.id == 742902329950470277, ctx.message.guild.roles)
    if ctx.message.author.id == 567561637951832083:
        True
    elif role in ctx.message.author.roles:
        if ctx.message.channel.name.startswith('ticket') or ctx.message.channel.id == 767108013752320020:
           True
        else:
           return
    elif ctx.message.channel.id == 869619078820659210 or ctx.message.channel.id == 1059112511967871036:
        True
    else:
        await ctx.send("Banning yourself from server in few seconds.")
        return
    if growid is None:
        await ctx.send("Growid ??")
        return
    data = getdata(growid)
    if data is None:
       await ctx.send(f"GrowID {growid} is not banned.")
       return
    status = data['banned']
    if status == "Yes":
      growid = data['player_name']
      by = data['banned_by']
      reason = data['banned_for']
      expire = data['ban_expires']
      await ctx.send(f"GrowID {growid} is banned by {by} for {reason} ban expires {expire}.")
      channel = bot.get_channel(983333089776390164)
      await channel.send(f"[LOGS] User {ctx.message.author} check ban {growid} and was banned by {by} for {reason}")
      return
    else:
      await ctx.send(f"GrowID {growid} is not banned.")
      return

@bot.command()
async def country(ctx, growid = None):
  gg = bot.get_guild(771352967277182976)
  role = discord.utils.find(lambda r: r.id == 776685936682729472, gg.roles)
  if ctx.message.author.id == 567561637951832083:
      True
#  elif role is not None:
  #    member = gg.get_member(ctx.message.author.id)
  #    if role in member.roles:
   #     True
  elif ctx.message.channel.id == 869619078820659210 or ctx.message.channel.id == 1059112511967871036:
     True
  elif ctx.message.guild.id == 1113163119573880933:
     True
  else:
      return
  if growid is None:
      await ctx.send("Growid ???")
      return
  data = getdata(growid)
  if data is None:
     await ctx.send(f"GrowID {growid} is not exist.")
     return
  ip = data['last_ip']
#  print(ip)
  try:
    ip = ip.replace("https:", "")
    ip = ip.replace("/", "")
    ip_api_response = requests.get(f"http://ip-api.com/json/{ip}") 
    json_ip_data = json.loads(ip_api_response.text)
    country = json_ip_data["country"]
    #print(json_ip_data["query"])
    if json_ip_data["query"] == "194.233.67.219":
      await ctx.send("bros country is invisible")
      return
    await ctx.send(f"bro is from {country}")
    # embed.add_field(name="ISP: ", value=json_ip_data["isp"], inline=False)
  except:
    await ctx.send('Unable to find bros country')

@verify.error 
async def verify_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
      wkwk = round(error.retry_after)
      await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.")
      return
    if isinstance(error, commands.errors.PrivateMessageOnly):
      await ctx.message.delete()
      await ctx.send(f'<@{ctx.message.author.id}>, Use this command in dm.')
      return
    if isinstance(error, commands.errors.CommandInvokeError):
      await ctx.send("Error.") 
      return

@bot.command()
@commands.dm_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def recovery(ctx, growid = None, *, emaillol = None):
      if growid is None:
        await ctx.send("Plase enter the growid.\nUsage : `!recovery <GrowID> <Email>`.")
        return
      if emaillol is None:
        await ctx.send("Please enter the email.\nUsage : `!recovery <GrowID> <Email>`.")
        return
      aa = os.path.exists(f"blacklistrecovery\{ctx.message.author.id}.txt")
      if aa == True:
        with open(f"blacklistrecovery\{ctx.message.author.id}.txt", "r") as j:
          wk = j.read()
          if wk == "2":
            await ctx.send("You are currently blacklisted from **recovery**. To appeal this reach our support in support channel.")
            return
      r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid})
      if r.status_code == 200:
        True
      else:
        await ctx.send("Recovery is currently unavailable.")
        return
      soup = BeautifulSoup(r.text, features='html.parser')
      values = [item.text.strip() for item in soup.select('.list')]
      if "Player was not found" in str(r.text):
        await ctx.send("That growid is not allowed.")
        return
      try:
        for ss in list(values):
          x = ss.split()
        email = x[3]
      except:
        await ctx.send("Error when fetching your email, please wait until this fixed.")
        return
      try:
        ip = ipaddress.ip_address(email)
        await ctx.send("Your account might be bugged, you can only manually recovery or report it to vyte.")
        logsagain = bot.get_channel(1036151353652826163)
        await logsagain.send(f"{ctx.message.author}({ctx.message.author.id}) tried to recovery \"{growid}\" but has their account broken (ip detected as email)")
        return
      except ValueError:
        pass
      if emaillol.lower() == email.lower():
        await ctx.send("Email is correct!")
        await ctx.send("Enter your new password.")
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel
        try:
          msg = await bot.wait_for("message", check=check, timeout=20)
        except asyncio.TimeoutError:
          await ctx.send("Canceled due to timer.")
          return
        newpass = msg.content
        await ctx.send(f"Your new password is {newpass}.")
        if growid.lower() == "vyte" or growid.lower() == "chris" or growid.lower() == "cyrus" or growid.lower() == "del" or growid.lower() == "zack" or growid.lower() == "kim" or growid.lower() == "zxooz":
         channel2 = bot.get_channel(1036151353652826163)
         await channel2.send(f"Faked changed growid **{growid}**.")
        else:
         r = requests.post("http://privategts1.eu:1338/r12rfwafga233ta/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': growid, 'changepass': 1, 'last_name': newpass})
        channel = bot.get_channel(1036151353652826163)
        embed=discord.Embed(description="**Recovery Logs**", color=0x32CD32)
        embed.set_author(name=ctx.message.author)
        embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Growid", value=growid, inline=True)
        embed.add_field(name="Requested Email", value=emaillol, inline=True)
        embed.add_field(name="Real Email", value=email, inline=True)
        embed.add_field(name="New Password", value=newpass, inline=True)
        embed.set_footer(text=f"ID : {ctx.message.author.id}")
        await channel.send(embed=embed)
        return
      else:
        if aa == False:
          f = open(f"blacklistrecovery\{ctx.message.author.id}.txt", "w")
          f.write("1")
          channel = bot.get_channel(1036151353652826163)
          embed=discord.Embed(description="**Wrong Email Recovery Logs**", color=0xFF0000)
          embed.set_author(name=ctx.message.author)
          embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=False)
          embed.add_field(name="Growid", value=growid, inline=True)
          embed.add_field(name="Requested Email", value=emaillol, inline=True)
          embed.add_field(name="Real Email", value=email, inline=True)
          embed.set_footer(text=f"ID : {ctx.message.author.id} | Attempt 1/2")
          await channel.send(embed=embed)
          await ctx.send("Please enter exact same email. (1/2)")
          return
        else:
          with open(f"blacklistrecovery\{ctx.message.author.id}.txt", "r") as o:
            qq = o.read()
            if qq == "1":
              f = open(f"blacklistrecovery\{ctx.message.author.id}.txt", "w")
              f.write("2")
              channel = bot.get_channel(1036151353652826163)
              embed=discord.Embed(description="**Wrong Email Recovery Logs**", color=0xFF0000)
              embed.set_author(name=ctx.message.author)
              embed.add_field(name="User", value=f"<@{ctx.message.author.id}>", inline=False)
              embed.add_field(name="Growid", value=growid, inline=True)
              embed.add_field(name="Requested Email", value=emaillol, inline=True)
              embed.add_field(name="Real Email", value=email, inline=True)
              embed.set_footer(text=f"ID : {ctx.message.author.id} | Attempt 2/2")
              await channel.send(embed=embed)
              await ctx.send("Please enter exact same email. (2/2)")
              return

@recovery.error 
async def recovery_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):
      wkwk = round(error.retry_after)
      await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.")
      return
    if isinstance(error, commands.errors.PrivateMessageOnly):
      await ctx.message.delete()
      await ctx.send(f'<@{ctx.message.author.id}>, Use this command in dm.')
      return
    if isinstance(error, commands.errors.CommandInvokeError):
      await ctx.send("Error.") 
      return

# @bot.command()
# async def verify2(ctx):
#     if ctx.message.guild.id == 771352967277182976:
#       if ctx.message.channel.id == 771352967277182984:
#         await ctx.message.delete()
#         ww = os.path.exists(f"verified\{ctx.message.author.id}_.txt")
#         if ww == True:
#           oo = open(f"verified\{ctx.message.author.id}_.txt", "r")
#           yy = oo.read()
#           if yy == ctx.message.author.name:
#             nicks = ''.join(choice((str.upper, str.lower))(c) for c in yy)
#             await ctx.message.author.edit(nick=nicks)
#           else: 
#             await ctx.message.author.edit(nick=yy)
#           role = get(ctx.guild.roles, name="Mod")
#           await ctx.author.add_roles(role)
#           channel = bot.get_channel(846249905441341441)
#           await channel.send(f" <@{ctx.message.author.id}> make sure read these mentioned **channels** <#771352967475363856> <#771352967475363857>")
#           log = bot.get_channel(1026125040430891018)
#           await log.send(f"Verified <@{ctx.message.author.id}>({ctx.message.author.id}) with growid {yy}.")
#         else:
#           await ctx.send(f"<@{ctx.message.author.id}>, You are not invited by bot, leave from this server and use ``!verify`` command.", delete_after=15)
#           log = bot.get_channel(1026125040430891018)
#           await log.send(f"Non registered user <@{ctx.message.author.id}>({ctx.message.author.id}) tried to verify.")
#           return

#@verify2.error 
#async def verify2_error(ctx, error):
 #   if isinstance(error, commands.errors.CommandInvokeError):
#      await ctx.send("Error.") 
#      return

@bot.command()
async def resetblacklist(ctx, user:discord.User = None):
  role = discord.utils.find(lambda r: r.id == 744347026635882616, ctx.message.guild.roles)
  if role in ctx.message.author.roles:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user.")
    return
  await ctx.send("Which one you wanna remove blacklist? `verify`/`recovery`.")
  check = lambda m: m.author == ctx.author and m.channel == ctx.channel
  try:
    msg = await bot.wait_for("message", check=check, timeout=15)
  except asyncio.TimeoutError:
    await ctx.send("Canceled due to timer.")
    return
  if msg.content.lower() == "verify":
    ww = os.path.exists(f"blacklist\{user.id}.txt")
    if ww == True:
      os.remove(f"blacklist\{user.id}.txt")
      await ctx.send(f"{user.name}'s verify failed attempt has been reseted.")
      channel = bot.get_channel(974256030454272001)
      await channel.send(f"[Logs] {ctx.message.author} reseted {user}({user.id})'s verify failed attempt.")
      return
    else:
      await ctx.send("That user doesn't have any verify failed attempt.")
      return
  if msg.content.lower() == "recovery":
    ww = os.path.exists(f"blacklistrecovery\{user.id}.txt")
    if ww == True:
      os.remove(f"blacklistrecovery\{user.id}.txt")
      await ctx.send(f"{user.name}'s recovery failed attempt has been reseted.")
      channel = bot.get_channel(1036151353652826163)
      await channel.send(f"[Logs] {ctx.message.author} reseted {user}({user.id})'s recovery failed attempt.")
      return
    else:
      await ctx.send("That user doesn't have any recovery failed attempt.")
      return
     

@resetblacklist.error 
async def resetblacklist_error(ctx, error):
  if isinstance(error, commands.errors.UserNotFound):
      await ctx.send("Can't find that user")
      return

@bot.command()
async def resetuser(ctx, user:discord.User = None):
  role = discord.utils.find(lambda r: r.id == 744347026635882616, ctx.message.guild.roles)
  if role in ctx.message.author.roles:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user.")
    return
  ww = os.path.exists(f"verified\{user.id}_.txt")
  if ww == True:
    os.remove(f"verified\{user.id}_.txt")
    await ctx.send(f"{user.name}'s verify has been reseted.")
    channel = bot.get_channel(745838712201412728)
    await channel.send(f"[Logs] {ctx.message.author} reseted {user}({user.id})'s verify attempt.")
  else:
    await ctx.send("That user doesn't have any verify attempt.")
    return

@resetuser.error 
async def resetuser_error(ctx, error):
  if isinstance(error, commands.errors.UserNotFound):
      await ctx.send("Can't find that user")
      return

@bot.command()
async def resetgrowid(ctx, growid = None):
  role = discord.utils.find(lambda r: r.id == 744347026635882616, ctx.message.guild.roles)
  if role in ctx.message.author.roles:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if growid is None:
    await ctx.send("Please enter the user.")
    return
  ww = os.path.exists(f"verified\{growid}_.txt")
  if ww == True:
    os.remove(f"verified\{growid}_.txt")
    await ctx.send(f"{growid}'s verify has been reseted.")
    channel = bot.get_channel(745838712201412728)
    await channel.send(f"[Logs] {ctx.message.author} reseted {growid}'s verify attempt.")
  else:
    await ctx.send("That growid doesn't have any verify attempt.")
    return
@resetgrowid.error 
async def resetgrowid_error(ctx, error):
  if isinstance(error, commands.errors.UserNotFound):
      await ctx.send("Can't find that growid")
      return

@bot.command()
async def poll(ctx, *, message):
    if ctx.message.author.id == 567561637951832083:
      True
    elif ctx.message.author.id == 616523087223062529:
      True
    else:
      return
    asd = await ctx.send(message)
    await asd.add_reaction('❎')
    await asd.add_reaction('✅')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    if isinstance(error, commands.CommandOnCooldown):
        return
    if isinstance(error, commands.errors.PrivateMessageOnly):
        return
    raise error

@bot.command()
async def dm(ctx, user:discord.User = None, *, message):
  if ctx.message.author.id == 567561637951832083:
    True
  else:
    return
  embed=discord.Embed(title="You've received a message", description=message, color=discord.Colour.random())
  embed.set_footer(text=f"in {ctx.message.author.guild}")
  try:
    await ctx.send('Dm sent')
    await user.send(embed=embed)
  except:
    await ctx.send('Can\'t dm that user maybe blocked')
    # await user.send(f'Someone sent you a message : {message} in {ctx.message.author.guild}')
  channel = bot.get_channel(983333074181951498) 
  embeds=discord.Embed(title="Logs", description=f'**{ctx.message.author.id} Sent :**\n{message} \n**To {user.id}**', color=discord.Colour.random())
  await channel.send(embed=embeds)
  return

@dm.error 
async def dm_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t dm that user')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
      await ctx.send('You need someone to dm')

@bot.command(aliases=['uptime'])
async def up(ctx):
  if ctx.message.author.id == 567561637951832083:
     True
  else:
     return
  await ctx.send(f"Up since <t:{bot.up}:R>")

@bot.command()
async def who(ctx, user:discord.User = None):
    if ctx.message.author.id == 567561637951832083:
        True
    else:
        return
    if user is None:
        user = ctx.message.author
    asd = round(user.created_at.timestamp())
    embed=discord.Embed(description=f"Created at <t:{asd}:F> \nID : {user.id}", color=discord.Colour.random())
    embed.set_author(name=user, icon_url=user.avatar)
    await ctx.send(embed=embed)

@who.error 
async def who_error(ctx, error):
  if isinstance(error, commands.errors.UserNotFound):
      await ctx.send("Can't find that user")
      return

@bot.command()
async def ban(ctx, user:discord.User = None, *, reason = None):
  role = discord.utils.find(lambda r: r.id == 742794591480184832, ctx.message.guild.roles)
  if role in ctx.message.author.roles:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user")
    return
  if reason is None:
    reason = "Unknown reason"
  guild = bot.get_guild(899948087387242526)
  user = await bot.fetch_user(user.id)
  #try:
    #already_banned = await guild.bans()
    #for member in already_banned:
      #if user in member:
        #await ctx.send(f"{user} is already banned in GTPS 3 Download Server")
        #return
  #except discord.NotFound:
    #True
  await guild.ban(user, reason=reason)
  await ctx.send(f"Banned {user} from GTPS 3 Download Server discord, reason : {reason}.")
  log = bot.get_channel(745838712201412728)
  embed=discord.Embed(description="**Member Banned || GTPS 3 Download Server**", color=0xFF0000)
  embed.set_author(name=user, icon_url=f"{user.avatar}")
  embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
  embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
  embed.add_field(name="Reason", value=reason, inline=True)
  embed.set_footer(text=f"ID : {user.id}")
  await log.send(embed=embed)

@ban.error 
async def ban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t find that user')
      return

@bot.command()
async def bans(ctx, user:discord.User = None, *, reason = None):
  if ctx.message.author.id == 567561637951832083:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user")
    return
  if reason is None:
    reason = "Unknown reason"
  guild = bot.get_guild(899948087387242526)
  user = await bot.fetch_user(user.id)
  #try:
   # already_banned = await guild.bans()
    #for member in already_banned:
     # if user in member:
       # await ctx.send(f"{user} is already banned in GTPS 3 Download Server")
       # return
  #except discord.NotFound:
    #True
  await guild.ban(user, reason=reason)
  await ctx.send(f"Banned {user} from GTPS 3 Download Server discord, reason : {reason}.")

@bot.command()
async def crossban(ctx, user:discord.User = None, *, reason = None):
  role = discord.utils.find(lambda r: r.id == 742794591480184832, ctx.message.guild.roles)
  bot.userbanned = None
  bot.userbanned2 = None
  if role in ctx.message.author.roles:
    True
  elif ctx.message.author.id == 338130528538460160:
    True
  elif ctx.message.author.id == 420584968566079508:
    True
  elif ctx.message.author.id == 792897995812765728:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user")
    return
  if reason is None:
    reason = "Unknown reason"
  guild = bot.get_guild(742792944079208540)
  guild2 = bot.get_guild(899948087387242526)
  user = await bot.fetch_user(user.id)
  #already_banned = await guild.bans()
  #for member in already_banned:
   # if user in member:
    #  await ctx.send(f"{user} is already banned in GTPS 3 Main Server.")
     # bot.userbanned = True
  #already_banned2 = await guild2.bans()
  #for member in already_banned2:
    #if user in member:
    #  await ctx.send(f"{user} is already banned in GTPS 3 Download Server.")
      #bot.userbanned2 = True
      #if bot.userbanned is not None:
      #  return
  if bot.userbanned is None:
    try:
      if ctx.message.guild.get_member(user.id) is not None:
         await user.send(f"You were banned from GTPS 3 Discord Servers, reason : {reason}.")
      else:
         await ctx.send("Unable to dm the user.")
      await guild.ban(user, reason=reason)
      await ctx.send(f"Banned {user} from GTPS 3 Main Server discord, reason : {reason}.")
      log = bot.get_channel(745838712201412728)
      embed=discord.Embed(description="**Member Banned || GTPS 3 Main Server**", color=0xFF0000)
      embed.set_author(name=user, icon_url=f"{user.avatar}")
      embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
      embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      embed.set_footer(text=f"ID : {user.id}")
      await log.send(embed=embed)
    except:
     True
    # await ctx.send(f"Unable to ban {user} in GTPS 3 Main Server.")
  if bot.userbanned2 is None:
    try:
      await guild2.ban(user, reason=reason)
      await ctx.send(f"Banned {user} from GTPS 3 Download Server discord, reason : {reason}.")
      log = bot.get_channel(745838712201412728)
      embed=discord.Embed(description="**Member Banned || GTPS 3 Download Server**", color=0xFF0000)
      embed.set_author(name=user, icon_url=f"{user.avatar}")
      embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
      embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      embed.set_footer(text=f"ID : {user.id}")
      await log.send(embed=embed)
    except:
     True
   #   await ctx.send(f"Unable to ban {user} from GTPS 3 Download Server.")

@crossban.error 
async def crossban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t find that user')
      return

@bot.command()
async def silentban(ctx, user:discord.User = None, *, reason = None):
  if ctx.message.author.id == 567561637951832083:
    True
  elif ctx.message.author.id == 338130528538460160:
   True
  elif ctx.message.author.id == 420584968566079508:
   True
  elif ctx.message.author.id == 514394370804285460:
   True
  elif ctx.message.author.id == 746620014039138405:
   True
  else:
   return
  if user is None:
    await ctx.send("Please enter the user")
    return
  if reason is None:
    reason = "Unknown reason"
  guild = bot.get_guild(742792944079208540)
  guild2 = bot.get_guild(899948087387242526)
  try:
    await guild.ban(user, reason=reason)
    await ctx.send(f"Silent Banned {user} from GTPS 3 Main Server discord, reason : {reason}.")
  except:
    await ctx.send(f"Unable to ban {user} in GTPS 3 Main Server.")
  try:
    await guild2.ban(user, reason=reason)
    await ctx.send(f"Silent Banned {user} from GTPS 3 Download Server discord, reason : {reason}.")
  except:
    await ctx.send(f"Unable to ban {user} from GTPS 3 Download Server.")

@silentban.error 
async def silentban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t find that user')
      return
    
@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def invite(ctx):
    embed=discord.Embed(description="\n**Important Links:**\n**[GTPS3 Server](https://discord.com/invite/gtps3)\n[Invite GTPS3 Bot](https://discord.com/api/oauth2/authorize?client_id=830229763171418163&permissions=378944&scope=bot)**", color=discord.Colour.random())
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/830229763171418163/f812bdf0a1a847ffb244a733c5ba43c1.png?size=1024")
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def hostpc(ctx):
    await ctx.send("**GTPS3 IP** : ```\n193.70.38.4 www.growtopia1.com\n51.161.161.24 www.growtopia2.com\n```\n**Host Tutorial** : ```\n- Press ⊞ Win+R (Windows Key + R) to open up the \"Run\" window.\n- Type C:\Windows\System32\drivers\etc in the textbox.```", file=discord.File("files/host.mp4"))
    #await ctx.send("Banning yourself in 5 seconds")

@hostpc.error
async def hostpc_error(ctx, error):
    wkwk = round(error.retry_after)
    await ctx.send(f"This command is in cooldown, try again in {wkwk} seconds.", delete_after=wkwk)
    
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def hostandroid(ctx):
    #await ctx.send("<#994540115579912302>")
    await ctx.send("**Host link** : https://www.mediafire.com/file/fi2laxdfp8upqvc/gtps3_2023/file \n\n**Tutorial** : ```1. Download Virtual Hosts.\n\n2. Install Virtual Hosts to your device.\n\n3. Download hosts file.\n\n4. Open Virtual Hosts and click on SELECT HOSTS FILE.\n\n5. Add the hosts file you downloaded.\n\n6. Click on the big white checkbox and make it green.\n\n7. Open Growtopia and connect!```\n\n**Virtual Host** :", file=discord.File("files/Virtual_Host.apk"))

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def hostandroid2(ctx):
    #await ctx.send("<#994540115579912302>")
    await ctx.send("```1. Download \"(No Root) Hosts GO\".\n\n2. Install \"(Not Root) Hosts GO\" to your device.\n\n3. Open Host GO and Click on \"Hosts Editor\".\n\n4. Click checkbox on the right, and Click \"Download Hosts File\".\n\n5. Type the link on bellow:\nhttps://bit.ly/androidgtps \n\n6. Click on \"Download and Apply\".\n\n7. Back and click on \"START\".\n\n8. Open Growtopia and Connect!```Host Link: https://bit.ly/androidgtps \n\nHosts Go: https://m.apkpure.com/id/no-root-hosts-go/dns.hosts.server.change/download")

@bot.command()
async def update2(ctx):
    #await ctx.send("<#994540115579912302>")
    if ctx.message.author.id == 567561637951832083:
     True
    elif ctx.message.author.id == 514394370804285460:
     True
    elif ctx.message.author.id == 420584968566079508:
     True
    else:
     return
    channel = bot.get_channel(864089537147699221)
    aw = open("files/update.txt", "r")
    awr = aw.read()
    embed=discord.Embed(color=0x00FF00) #00FF00 green #FF0000 red
    embed.add_field(name="Update History", value=f"Last bot's database update <t:{awr}:R>.")
    embed.set_footer(text="This mean if you bought mod after last update then wait until next update.")
    message = await channel.fetch_message(1028299798014595142)
    await message.edit(embed=embed)
    await ctx.send("Done")


@hostandroid.error
async def hostandroid_error(ctx, error):
    wkwk = round(error.retry_after)
    await ctx.send(f"This command is in cooldown, try again in {wkwk} seconds.", delete_after=wkwk)

@hostandroid2.error
async def hostandroid2_error(ctx, error):
    wkwk = round(error.retry_after)
    await ctx.send(f"This command is in cooldown, try again in {wkwk} seconds.", delete_after=wkwk)

@invite.error
async def invite_error(ctx, error):
    wkwk = round(error.retry_after)
    await ctx.send(f"You are in cooldown, try again in {wkwk} seconds.", delete_after=wkwk)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def hostios(ctx):
    await ctx.send("**Surge 4 link** : https://apps.apple.com/app/surge-4/id1442620678 \n\n**Host Link** : https://bit.ly/iosgtps \n\n** Tutorial** : \n1 - Download App called: Surge 4 from App Store. https://apps.apple.com/app/surge-4/id1442620678\n\n2 - Press \"OK\".\n\n3 - Click on \"Default.conf\".\n\n4 - Click on \"IMPORT\" part -> Download Profile from URL.\n\n5 - Put url \"https://bit.ly/iosgtps\" and click \"OK\" and \"Done\"\n\n6 - Press \"SETUP\" and then agree to policy by clicking \"OK\" and \"Allow\" for VPN Configuration!.\n\n7 - Done, then open \"Growtopia\" and Connect!")

@hostios.error
async def hostios_error(ctx, error):
    wkwk = round(error.retry_after)
    await ctx.send(f"This command is in cooldown, try again in {wkwk} seconds.", delete_after=wkwk)

@bot.command()
async def updatedata(ctx):
    #print("downloading document")
      await ctx.send("Send a items.dat file")
      check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await bot.wait_for("message", check=check, timeout=30)
      except asyncio.TimeoutError:
        await ctx.send("Canceled due to time")
        return
      files = []
      for attachment in msg.attachments:
        if attachment.filename == "items.dat":
         # response = requests.get(attachment.url).content
          #DOWNLOAD_PATH = "C:\Users\Administrator\Desktop\bot"
          ww = os.path.exists("items.dat")
          if ww == True:
            os.remove("items.dat")
          await ctx.send('Updating items.dat')
          await attachment.save(attachment.filename)
          os.environ['PATH'] += os.pathsep + 'C:\\MinGW\\bin\\'
         # os.system("decoder items.dat")
          #await ctx.send("Currently disabled, update manualy open cmd in bot folder, type ``decoder items.dat``.")
          #response = requests.get(attachment.url).content
         # hh = open("items.dat", "w")
         # hh.write(str(response))
          decoder_path = "files/decoder.exe"
          items_dat_path = "items.dat"
          command = f"{decoder_path} {items_dat_path}"
          result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          await ctx.send("Done", file=discord.File("files/itemsid.json"))
          await ctx.send(file=discord.File("files/itemsid2.json"))
          await ctx.send(file=discord.File("files/itemsid3.txt"))
          return
        else:
          await ctx.send("Cancled, Send a file with name ``items.dat``")
          await msg.add_reaction("❌")
          return
      if msg.content == "Cancel":
        await ctx.send("Canceled")
        return
      else:
        await ctx.send("Canceled")
    # files = []
    # for attachment in ctx.message.attachments:
    #    True
       #await attachment.save(attachment.filename)
    # response = requests.get(attachment.url).content
    # asd = decFile(response)
    #print(f"success name {asd}")

@bot.command()
async def unban(ctx, user:discord.User = None, *, reason = None):
  role = discord.utils.find(lambda r: r.id == 742794591480184832, ctx.message.guild.roles)
  if role in ctx.message.author.roles:
    True
  else:
    await ctx.send("You dont have permission to use this command.")
    return
  if user is None:
    await ctx.send("Please enter the user")
    return
  if reason is None:
    reason = "Unknown reason"
  guild = bot.get_guild(899948087387242526)
  banned_users = await guild.bans()
  for ban_entry in banned_users:
    try:
      await guild.unban(user)
      user = await bot.fetch_user(user.id)
      await ctx.send(f"Unbanned {user} from GTPS 3 Download Server discord, reason : {reason}.")
      log = bot.get_channel(745838712201412728)
      embed=discord.Embed(description="**Member Unbanned || GTPS 3 Download Server**", color=0xFFFF00)
      embed.set_author(name=user, icon_url=f"{user.avatar}")
      embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
      embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      embed.set_footer(text=f"ID : {user.id}")
      await log.send(embed=embed)
      return
    except:
      await ctx.send(f"{user} is not banned in GTPS 3 Download Server.")
      return

@unban.error 
async def unban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t find that user')
      return

@bot.command()
async def crossunban(ctx, user:discord.User = None, *, reason = None):
    role = discord.utils.find(lambda r: r.id == 742794591480184832, ctx.message.guild.roles)
    if role in ctx.message.author.roles:
      True
    elif ctx.message.author.id == 338130528538460160:
      True
    elif ctx.message.author.id == 420584968566079508:
      True
    else:
      await ctx.send("You dont have permission to use this command.")
      return
    if user is None:
      await ctx.send("Please enter the user")
      return
    if reason is None:
      reason = "Unknown reason"
    guild = bot.get_guild(742792944079208540)
    #log = bot.get_channel(745838712201412728)
    #banned_users = await guild.bans()
    unbanned = False
    try:
     # user = await bot.fetch_user(user.id)
      await guild.unban(user)
      await ctx.send(f"Unbanned {user} from GTPS 3 Main Server discord, reason : {reason}.")
      log = bot.get_channel(745838712201412728)
      unbanned = True
      embed=discord.Embed(description="**Member Unbanned || GTPS 3 Main Server**", color=0xFFFF00)
      embed.set_author(name=user, icon_url=f"{user.avatar}")
      embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
      embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      embed.set_footer(text=f"ID : {user.id}")
      await log.send(embed=embed)
    except:
     #True
      if unbanned == False:
       await ctx.send(f"{user} is not banned in GTPS 3 Main Server.")
    guild2 = bot.get_guild(899948087387242526)
    #banned_users = await guild2.bans()
  # for ban_entry in banned_users:
    unbanned2 = False
    try:
      user = await bot.fetch_user(user.id)
      await guild2.unban(user)
      unbanned2 = True
      await ctx.send(f"Unbanned {user} from GTPS 3 Download Server discord, reason : {reason}.")
      log = bot.get_channel(745838712201412728)
      embed=discord.Embed(description="**Member Unbanned || GTPS 3 Download Server**", color=0xFFFF00)
      embed.set_author(name=user, icon_url=f"{user.avatar}")
      embed.add_field(name="User", value=f"<@{user.id}>", inline=True)
      embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=True)
      embed.add_field(name="Reason", value=reason, inline=True)
      embed.set_footer(text=f"ID : {user.id}")
      await log.send(embed=embed)
      return
    except:
      if unbanned2 == False:
        await ctx.send(f"{user} is not banned in GTPS 3 Download Server.")
        return

@crossunban.error 
async def crossunban_error(ctx, error):
    if isinstance(error, commands.errors.UserNotFound):
      await ctx.send('Can\'t find that user')
      return

@bot.command()
async def online(ctx):
    if ctx.message.author.id == 567561637951832083:
        True
    else:
        return
    with open('files/status.txt', 'r') as y:
        if 'online' in y:
            await ctx.send('status already online')
            return
        else:
            with open('files/status.txt', 'w') as s:
                s.write('online')
                await bot.change_presence(status=discord.Status.online)
                await ctx.send('changed status to online')

@bot.command()
async def idle(ctx):
    if ctx.message.author.id == 567561637951832083:
        True
    else:
        return
    with open('files/status.txt', 'r') as y:
        if 'idle' in y:
            await ctx.send('status already idle')
            return
        else:
            with open('files/status.txt', 'w') as s:
                s.write('idle')
                await bot.change_presence(status=discord.Status.idle)
                await ctx.send('changed status to idle')

@bot.command()
async def dnd(ctx):
    if ctx.message.author.id == 567561637951832083:
        True
    else:
        return
    with open('files/status.txt', 'r') as y:
        if 'dnd' in y:
            await ctx.send('status already dnd')
            return
        else:
            with open('files/status.txt', 'w') as s:
                s.write('dnd')
                await bot.change_presence(status=discord.Status.dnd)
                await ctx.send('changed status to dnd')

@bot.command()
async def offline(ctx):
    if ctx.message.author.id == 567561637951832083:
        True
    else:
        return
    with open('files/status.txt', 'r') as y:
        if 'offline' in y:
            await ctx.send('status already offline')
            return
        else:
            with open('files/status.txt', 'w') as s:
                s.write('offline')
                await bot.change_presence(status=discord.Status.offline)
                await ctx.send('changed status to offline')

#keep_alive()
#bot.loop.create_task(update_status())
bot.run("TOKEN_BOT")