import re

mac_table = '166    54a2.74f7.0326    DYNAMIC     Gi1/0/11'

pattern = r'(\d+)\s+([\da-f]{4}\.[\da-f]{4}\.[\da-f]{4})\s+(\w+)\s+(\S+)'
match = re.match(pattern, mac_table)

fmt = "{:<6}: {}"
print(fmt.format("VLAN", match.group(1)))
print(fmt.format("MAC", match.group(2)))
print(fmt.format("Type", match.group(3)))
print(fmt.format("Port", match.group(4)))