import re
asa_conn = "TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO\nTCP\
            Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"

print(asa_conn.split('\n'))

asa_dict = {}
pattern = r'TCP\s+\w+\s+([\d.]+):(\d+)\s+\w+\s+([\d.]+):(\d+),\s+idle\s+[^,]+, bytes (\d+), flags (\w+)'
for conn in asa_conn.split('\n'):
    m = re.match(pattern, conn)
    if m:
        key = (m.group(1), m.group(2), m.group(3), m.group(4))
        val = (m.group(5), m.group(6))
        asa_dict[key] = val

print("打印分析後的字典")
print()
print(asa_dict)


print()
print("格式化打印輸出")
print()

for key, value in asa_dict.items():
    src_ip, src_port, dst_ip, dst_port = key
    bytes_val, flags = value
    print(f'{"src":<10}: {src_ip:<16} | {"src_port":<10}: {src_port:<6} | {"dst":<10}: {dst_ip:<16} | {"dst_port":<10}: {dst_port:<6}')
    print(f'{"bytes":<10}: {bytes_val:<16} | {"flags":<10}: {flags:<6}')
    print("=" * 90)