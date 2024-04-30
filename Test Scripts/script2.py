import re

text = "6@Cyrus*2025-04-26 13:00:20"

pattern = re.compile(r'^(\S+)\t([^\d]+)')

result = {}
for match in pattern.finditer(text):
    user, reason = match.groups()
    result[user] = reason.strip()

for user, reason in result.items():
    output = f'Banned by `{user}`, reason {reason}'
    print(output)
