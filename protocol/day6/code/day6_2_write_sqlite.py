import sys
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code.day6_1_create_db import InternfaceMonitor, engine
from code.tools.day6_get_all import snmpv2_get_all
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

DEVICES = [
    ('10.10.1.1', 'qytangro'),
    ('10.10.1.2', 'qytangro'),
]

# ifDescr = '1.3.6.1.2.1.2.2.1.2'
# ifInOctets = '1.3.6.1.2.1.2.2.1.10'
# ifOutOctets = '1.3.6.1.2.1.2.2.1.16'

def collect_and_write():
    session = Session()
    records = []

    for ip, community in DEVICES:
        try:
            result = snmpv2_get_all(ip, community)
            if_list = result.get('interface_list', [])
   
            for iface in if_list:
                name      = iface['interface_name']
                in_bytes  = iface['in_bytes']
                out_bytes = iface['out_bytes']

                if in_bytes == 0 and out_bytes == 0:
                    print(f'[~] {ip} {name:<30} 無流量, 跳過')
                    continue

                record = InternfaceMonitor(
                    device_ip=ip,
                    interface_name=name,
                    in_bytes=in_bytes,
                    out_bytes=out_bytes
                )
                records.append(record)
                print(f'[+] {ip} {name:<30} IN={in_bytes:>12} OUT={out_bytes:>12}')
        except Exception as e:
            print(f'[-] {ip}: 採集失敗 - {e}')
    if records:
        session.add_all(records)
        session.commit()
        print(f'[*] 共寫入 {len(records)} 條紀錄')
    session.close()

if __name__ == '__main__':
    collect_and_write()
