import re
import os

result = os.popen("ifconfig eth0").read()

ip        = re.search(r'inet ([\d.]+)', result).group(1)
netmask   = re.search(r'netmask ([\d.]+)', result).group(1)
broadcast = re.search(r'broadcast ([\d.]+)', result).group(1)
mac       = re.search(r'ether ([\w:]+)', result).group(1)
 
fmt = "{:<10}: {}"
# print(fmt.format("IP", ip))
print(fmt.format("Netmask", netmask))
print(fmt.format("Broadcast", broadcast))
print(fmt.format("MAC", mac))
print(f'{"IP":<10}: {ip}')

gateway = ".".join(ip.split(".")[:2]) + ".0.1"
ping_result = os.popen("ping -c 1 -w 1 " + gateway).read()

print()
print("假設網關為: " + gateway)
if "1 received" in ping_result or "1 packets received" in ping_result:
    print("Ping " + gateway + " ... reachable")
else:
    print("Ping " + gateway + " ... unreachable")