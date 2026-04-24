from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from day4_1_create_db import RouterMonitor, engine
from tools.day4_bokeh_line import bokeh_line


def show_cpu_mem_from_db(hours=1):
    Session = sessionmaker(bind=engine)
    session = Session()

    cutoff = datetime.now() - timedelta(hours=hours)

    DEVICE_IPS = [
        ip[0]
        for ip in session.query(RouterMonitor.device_ip)
        .filter(RouterMonitor.record_datetime >= cutoff)
        .distinct()
        .all()
    ]
    cpu_lines = []
    mem_lines = []

    for idx, ip in enumerate(DEVICE_IPS, start=1):
        records = (session.query(RouterMonitor).filter(RouterMonitor.record_datetime >= cutoff,
                                                       RouterMonitor.device_ip == ip)
                   .order_by(RouterMonitor.record_datetime)
                   .all())
        if not records:
            print(f'[!] {ip}: 最近 {hours} 小時無數據')
            continue
        time_list = [r.record_datetime for r in records]
        cpu_list = [r.cpu_useage_percent for r in records]
        mem_list = [round(r.mem_use / (r.mem_use + r.mem_free) * 100, 2)
                    for r in records]

        cpu_lines.append([time_list, cpu_list, ip])
        mem_lines.append([time_list, mem_list, ip])

        print(f'[*] 設備IP{idx} ({ip}): 讀取 {len(records)} 條紀錄')
    session.close()

    if cpu_lines:
        bokeh_line(cpu_lines, title='CPU利用率趨勢')
    else:
        print(f'[!] CPU無資料')
    if mem_lines:
        bokeh_line(mem_lines, title='內存利用率趨勢')
    else:
        print(f'[!] 內存無資料')


if __name__ == '__main__':
    show_cpu_mem_from_db()