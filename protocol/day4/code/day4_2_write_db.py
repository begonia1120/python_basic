import sys,os,asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from code.day4_1_create_db import RouterMonitor, engine
from code.tools.day4_get import snmpv2_get
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

DEVICES = [
    ('10.10.1.1', 'qytangro'),
    ('10.10.1.2', 'qytangro'),
]

OID_CPU_5SEC = '1.3.6.1.4.1.9.9.109.1.1.1.1.6.7'
OID_MEM_USED = '1.3.6.1.4.1.9.9.109.1.1.1.1.12.7'
OID_MEM_FREE = '1.3.6.1.4.1.9.9.109.1.1.1.1.13.7'

def collect_and_write():
    session = Session()
    records = []

    for ip, community in DEVICES:
        try:
            _, cpu_str = asyncio.run(snmpv2_get(ip, community, OID_CPU_5SEC))
            _, mem_used_str = asyncio.run(snmpv2_get(ip, community, OID_MEM_USED))
            _, mem_free_str = asyncio.run(snmpv2_get(ip, community, OID_MEM_FREE))

            record = RouterMonitor(
                device_ip=ip,
                cpu_useage_percent=int(cpu_str),
                mem_use=int(mem_used_str),
                mem_free=int(mem_free_str)
            )
            records.append(record)
            print(f'[+] {ip}: CPU={cpu_str}%, MEM_Used={mem_used_str}, MEM_Free={mem_free_str}')
        except Exception as e:
            print(f'[-] {ip}: 採集失敗 - {e}')
    if records:
        session.add_all(records)
        session.commit()
        print(f'[*] 共寫入 {len(records)} 條紀錄')
    session.close()

if __name__ == '__main__':
    collect_and_write()


