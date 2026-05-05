import sys,os,asyncio
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from code.tools.snmp_v2_1_get import snmpv2_get
from code.tools.snmp_v2_3_getbulk import snmpv2_getbulk

# ~~~~~~~~~~~~~~~~注意版本~~~~~~~~~~~~~
# pyasn1==0.6.1    # ~~~更新时间2025/2/23
# pysnmp==7.1.16   # ~~~更新时间2025/2/23


# SNMP v2 获取信息汇总
def snmpv2_get_all(ip_address, community):
    # 主机名
    sys_name = asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.5.0", port=161))[1]

    # cpmCPUTotal5sec
    # 实体实时的CPU使用率 取值范围：0～100 缺省值：0
    cpu_usage = int(asyncio.run(snmpv2_get(ip_address,
                                           community,
                                           "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7",
                                           port=161))[1])
    # print(cpu_usage)
    # cpmCPUMemoryUsed
    mem_used = int(asyncio.run(snmpv2_get(ip_address,
                                          community,
                                          "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7",
                                          port=161))[1])
    # cpmCPUMemoryFree
    mem_free = int(asyncio.run(snmpv2_get(ip_address,
                                          community,
                                          "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7",
                                          port=161))[1])

    mem_percent = (round(mem_used / (mem_used + mem_free), 4)) * 100

    # print(mem_percent)

    # -----------------------------------------------------
    # 接口名称
    raw_name_list = asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.2", port=161))
    if_name_list = [raw_if_name[1] for raw_if_name in raw_name_list]
    # print(if_name_list)

    # 接口速率
    raw_speed_list = asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.5", port=161))
    if_speed_list = [raw_speed[1] for raw_speed in raw_speed_list]
    # print(if_speed_list)

    # 获取接口管理状态
    raw_status_list = asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.7", port=161))
    if_status_list = [raw_status[1] for raw_status in raw_status_list]
    # print(if_status_list)

    # 进接口字节数
    raw_in_bytes_list = asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.10", port=161))
    if_in_bytes_list = [raw_in_bytes[1] for raw_in_bytes in raw_in_bytes_list]
    # print(if_in_bytes_list)

    # 出接口字节数
    raw_out_bytes_list = asyncio.run(snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.16", port=161))
    if_out_bytes_list = [raw_out_bytes[1] for raw_out_bytes in raw_out_bytes_list]
    # print(if_out_bytes_list)

    interface_list = []
    for name, speed, status, in_bytes, out_bytes in zip(if_name_list, if_speed_list, if_status_list, if_in_bytes_list, if_out_bytes_list):
        if int(in_bytes) and int(out_bytes):
            interface_list.append({
                'interface_name': name,
                'interface_speed': int(speed),
                'interface_status': True if status == '1' else False,
                'in_bytes': int(in_bytes),
                'out_bytes': int(out_bytes)
            })

    return {'device_ip': ip_address,
            'hostname': sys_name,
            'cpu_usage': cpu_usage,
            'mem_usage_percent': mem_percent,
            'mem_usage': mem_used,
            'mem_free': mem_free,
            'interface_list': interface_list
            }


if __name__ == "__main__":
    # ~~~~~~~~~~~~~~~~注意版本~~~~~~~~~~~~~
    # pyasn1==0.6.1    # ~~~更新时间2025/2/23
    # pysnmp==7.1.16   # ~~~更新时间2025/2/23

    # 使用Linux解释器 & WIN解释器

    # ip地址与snmp community字符串
    from pprint import pprint
    ip_address = "10.10.1.2"
    community = "qytangro"
    pprint(snmpv2_get_all(ip_address, community))
