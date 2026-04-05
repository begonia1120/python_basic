import hashlib
import os
import time
import re

from day9_task1 import ssh_run

def get_config(host, username, password):
    output = ssh_run(host, username, password, 'show running-config')
    match = re.search(r'(hostname[\s\S]+end)', output)
    return match.group(1) if match else ''

def monitor_config(host, username, password, interval=5):
    config = get_config(host, username, password)
    last_md5 = hashlib.md5(config.encode()).hexdigest()
    print(f'[*] 當前配置 MD5: {last_md5}')

    while True:
        time.sleep(interval)
        config = get_config(host, username, password)
        current_md5 = hashlib.md5(config.encode()).hexdigest()
        if current_md5 == last_md5:
            print(f'[*] 當前配置 MD5: {current_md5}')
        else:
            print(f'[!] 告警: 配置已改變! 新 MD5: {current_md5}')
            break

if __name__ == '__main__':
    monitor_config('10.10.1.1', 'admin', 'Cisc0123')