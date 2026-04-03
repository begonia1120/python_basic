import os
import shutil

os.makedirs('backup', exist_ok=True)

files = {
    'R1_config.txt': 'hostname R1\ninterface GigabitEthernet0/0\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R2_config.txt': 'hostname R2\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'R3_config.txt': 'hostname R3\ninterface GigabitEthernet0/0\n no shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
    'SW1_config.txt': 'hostname SW1\ninterface Vlan1\n shutdown\ninterface GigabitEthernet0/1\n no shutdown\n',
}


for file_name, content in files.items():
    filepath = os.path.join('backup', file_name)
    with open(filepath, 'w') as f:
        f.write(content)

print("發現包含 shutdown 接口的設備配置文件:")

for filename in sorted(os.listdir('backup')):
    filepath = os.path.join('backup', filename)
    with open(filepath, 'r') as f:
        for line in f:
            if 'shutdown' in line and 'no shutdown' not in line:
                print(filename)
                break

shutil.rmtree('backup')
print("backup/ 目錄已清理")

# files = {
#     'R1_config.txt': """hostname R1
# interface GigabitEthernet0/0
#    shutdown
# interface GigabitEthernet0/1
#    no shutdown
# """,
#     'R2_config.txt': """hostname R2
# interface GigabitEthernet0/0
#    no shutdown
# interface GigabitEthernet0/1
#    no shutdown
# """,
#     'R3_config.txt': """hostname R3
# interface GigabitEthernet0/0
#    no shutdown
# interface GigabitEthernet0/1
#    no shutdown
# """,
#     'sw1_config.txt': """hostname SW1
# interface Vlan1
#    shutdown
# interface GigabitEthernet0/1
#    no shutdown
# """,
# }