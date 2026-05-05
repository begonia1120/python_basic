#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import sys

from sqlalchemy.sql.functions import current_time
sys.path.extend(['/python_basic/'])

from protocol.day4.code.day4_get_all import snmpv2_get_all
import datetime
from influxdb import InfluxDBClient

ip_list =['10.10.1.1', '10.10.1.2']
snmp_community = 'qytangro'

influx_host_ip = '10.10.1.200'
client = InfluxDBClient(influx_host_ip, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')

record_list = []

for router_ip in ip_list:
    getall_result = snmpv2_get_all(router_ip, snmp_community)
    current_time = datetime.datetime.now(datetime.UTC).isoformat("T")
    cpu_mem_body = {
                    'measurement': 'router_monitor',
                    'time': current_time,
                    'tags': {
                        'device_ip': getall_result.get('device_ip'),
                        'device_type': 'IOS-XE'
                        },
                    'fields': {
                        'cpu_usage': getall_result.get('cpu_usage'),
                        'mem_usage': getall_result.get('mem_usage'),
                        'mem_free': getall_result.get('mem_free'),
                    },
                }
    record_list.append(cpu_mem_body)

client.write_points(record_list)
                   