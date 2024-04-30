import requests
from bs4 import BeautifulSoup
import os
import time
import re
#os.system("cls")

r = requests.post("http://privategts1.eu:1338/iwiaoaoaoao99191919/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php", data={'first_name': 'zack'})
if r.status_code == 200:
  True
else:
  print("DOWN")
print(r.status_code)
soup = BeautifulSoup(r.text, features='html.parser')
values = [item.text.strip() for item in soup.select('.list')]
for ss in list(values):
 print(ss)
 x = ss.split()
print(x)
name = x[2]
email = x[3]
ip = x[4]
mac = x[5]
fa = x[7]
rid = x[8]
long = x[13]
gg = x[14]
print(long)
long = (f"{long} {gg}")
#print(long)
print(r.status_code)
#pattern = re.compile(r'(\d+@[\w]+)``([\w]+)')
for line in long.split('\n'):
    match = re.match(r'^(\S+)\t([^\d]+)', line)
    if match:
        by, reason = match.groups()
print(f"By {by} and reason {reason}")
#result = {}
#for match in pattern.finditer(long):
 #   user, reason = match.groups()
  #  result[user] = reason

#for user, reason in result.items():
 #   output = f'banned by {user}, reason {reason}'
 #   print(output)
print(long)
#print(f"name {name}, email {email}, ip {ip}, mac {mac}, 2fa {fa}, rid {rid}, {long}")
 #data = item.text
 #gg = ["data1", "data2", "data3", "data4", "data5", "data6", "data7", "data8", "data9", "data10", "data11", "data12", "data13", "data14", "data15"]
#print(f"lol {data}")