import re

conn = 'TCP server  172.16.1.101:443 localserver  172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

#print(conn.split())

#pattern = r'(\w+)\s+\w+\s+([\d.]+):(\d+)\s+\w+\s+([\d.]+):(\d+)'
pattern = r'(?P<Protocol>\w+)\s+\w+\s+' \
          r'(?P<Server_IP>[\d.]+):(?P<Server_Port>\d+)\s+\w+\s+' \
          r'(?P<Client_IP>[\d.]+):(?P<Client_Port>\d+)'
match = re.match(pattern, conn)

fmt = "{:<12}: {}"
print(f'{"Protocol":<12}: {match.group("Protocol")}')
print(fmt.format("Server IP", match.group('Server_IP')))
print(fmt.format("Server Port", match.group('Server_Port')))
print(fmt.format("Client IP", match.group('Client_IP')))
print(fmt.format("Client Port", match.group('Client_Port')))