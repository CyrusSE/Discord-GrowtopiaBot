import glob
import os

path = './price'

for filename in glob.glob(os.path.join(path, '*.json')):
    try:
        with open(filename, 'r+') as file:
            content = file.read()
            if "jvDj7xz&i€8&>VvF5!W3EcP^}?G$S#0001" in content:
                content = content.replace("jvDj7xz&i€8&>VvF5!W3EcP^}?G$S#0001", "738445498444284056")
                file.seek(0)  
                file.write(content)
                file.truncate()  
                print(f"Replaced text in file: {filename}")
    except:
        continue

