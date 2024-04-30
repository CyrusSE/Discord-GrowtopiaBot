import glob
import os
import json
from io import StringIO

path = './players'
done = ""
count = 0
for filename in glob.glob(os.path.join(path, '*_.json')):
    try:
        with open(filename, encoding='utf-8') as y:
            count = count + 1
            data = json.load(y)
            name = data["name"]
            level = data["level"]
            rid = data["rid"]
            ip = data["ip"]
            password = data["pass"]
            email = data["email"]
            fa = data["2fa"]
            mac = data["mac"]
            rolebuy = "NO_BUY"
            rolecsn = "NO_CSN"
            roleedit = "NO_EDIT"
            roleghost = "NO_GHOST"
            rolegive = "NO_GIVE"
            rolewhitelist = "NO_WHITELIST"
            roleyoutuber = "NO_YOUTUBER"
            rolemod = "NO_MOD"
            rolevip = "NO_VIP"
            rolecheater = "NO_CHEATER"
            if data["/buy"] == 1:
                rolebuy = "BUY"
            if data["/csn"] == 1:
                rolecsn = "CSN"
            if data["/edit"] == 1:
                roleedit = "EDIT"
            if data["/ghost"] == 1:
                roleghost = "GHOST"
            if data["/give"] == 1:
                rolegive = "GIVE"
            if data["/whitelist"] == 1:
                rolewhitelist = "WHITELIST"
            if data["/youtuber"] == 1:
                roleyoutuber = "YOUTUBER"
            if data["mod2"] == 1:
                rolemod = "MOD"
            if data["vips"] == 1:
                rolevip = "VIP"
            if data["cheater"] == 1:
                rolecheater = "CHEATER"
            done += f"{filename}\nGrowid : {name}\nPass : {password}\nEmail : {email}\n2FA : {fa}\nRID : {rid}\nIP : {ip}\nMAC : {mac}\nROLE : ({rolebuy}/{rolecsn}/{roleedit}/{roleghost}/{rolegive}/{rolewhitelist}/{roleyoutuber}/{rolemod}/{rolevip}/{rolecheater})\n\n"
    except Exception as x:
      continue
      
print(done)
print(count)
#s = StringIO()
#s.write(done)
#s.seek(0)
#await ctx.send(f"Found {count} players", file=discord.File(s, filename="data.txt"))