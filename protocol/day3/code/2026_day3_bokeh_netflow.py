import re
from protocol.day3.code.tools.day3_ssh_single_cmd import ssh_run
from protocol.day3.code.tools.day3_bokeh_bing import bokeh_bing

def get_netflow_app(host, username, password):
    show_result = ssh_run(host, username, password, 'show flow monitor name qytang-monitor cache format table')
    print(show_result)

    app_name_list = []
    app_bytes_list = []

    for line in show_result.strip().split('\n'):
        match = re.match(r'^((port|layer7|port)\s+\S+)\s+(\d+)\s*$', line)
        if match:
            app_name_list.append(match.group(1).strip())
            app_bytes_list.append(match.group(3))
    
    print(f'[*] 提取到 {len(app_name_list)} 條 Netflow 紀錄')
    for name, byt in zip(app_name_list, app_bytes_list):
        print(f'     {name:<25s} {byt} bytes')

    bokeh_bing(app_name_list, app_bytes_list, 'Netflow應用流量分布')

if __name__ == "__main__":
    get_netflow_app('10.10.1.1', 'admin', 'Cisc0123')