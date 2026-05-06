#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import sys

from sqlalchemy.sql.functions import current_time
sys.path.extend(['/python_basic/'])

from protocol.day6.code.tools.day6_get_all import snmpv2_get_all
import datetime
from influxdb import InfluxDBClient

ip_list =['10.10.1.1', '10.10.1.2']
snmp_community = 'qytangro'

influx_host_ip = '10.10.1.200'
client = InfluxDBClient(influx_host_ip, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')

record_list = []

for router_ip in ip_list:
    result = snmpv2_get_all(router_ip, snmp_community)
    current_time = datetime.datetime.now(datetime.UTC).isoformat("T")
    interface_list = result.get('interface_list', [])
    for interface in interface_list:
        in_b  = interface.get('in_bytes', 0)
        out_b = interface.get('out_bytes', 0)
        if in_b == 0 and out_b == 0:
            print(f'[~] {router_ip} {interface.get('interface_name')} 無流量, 跳過')
            continue
        interface_info_body = {
            'measurement': 'interface_monitor',
            'time': current_time,
            'tags': {
                'device_ip': result.get('device_ip'),
                'interface_name': interface.get('interface_name'),
                'device_type': 'IOS-XE'
            },
            'fields': {
                'in_bytes': interface.get('in_bytes'),
                'out_bytes': interface.get('out_bytes')
            },
        }
        print(interface_info_body)
        record_list.append(interface_info_body)

client.write_points(record_list)
                   