#import sys
import os

from day8_task2 import ping_check
from day9_task1 import ssh_run

def collect_interfaces(ip_list, username='admin', password='Cisc0123'):
    for ip in ip_list:
        reachable, _ = ping_check(ip)
        if not reachable:
            print(f'[x] {ip} 不可達, 跳過')
            continue
        print(f'[*] {ip} 可達, 正在採集...')
        output = ssh_run(ip, username, password, 'show ip interface brief')
        print(f'---------- {ip} 接口信息 ----------')
        print(output.strip())
        print()

if __name__ == '__main__':
    devices = ['10.10.1.1', '10.10.1.2', '10.10.1.3']
    collect_interfaces(devices)