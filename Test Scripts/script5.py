import requests
from bs4 import BeautifulSoup


def scrape_table_columns(growid):
    url = ("http://privategts1.eu:1338/iwiaoaoaoao99191919/gewa8gwea94g9weag489weag/561ggawe61gawgt.geawg/panel/editplayer.php")
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
growid = "awtiohjaowithiowahowaih"
if growid is None:
   print("not exist")
table_data = scrape_table_columns(growid)
if table_data is None:
   print("not exist")
if table_data:
    print(table_data)
    print(table_data['email'])
    print(table_data['banned'])
    print(table_data['banned_by'])
    print(table_data['banned_for'])
else:
    print("not exist")