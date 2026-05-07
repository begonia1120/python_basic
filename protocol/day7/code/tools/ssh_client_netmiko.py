from netmiko import Netmiko

def netmiko_show_cred(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet'
                    #'secert': enable
                    # 'global_delay_factor': 2,  # 增加全局延迟因子
                    # 'session_log': 'session.log',  # 启用会话日志
                    # 'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return

def netmiko_config_cred(host, username, password, cmds_list, enable='Cisc0123', ssh=True, verbose=False):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet'
                    #'secert': enable
                    # # 'global_delay_factor': 2,  # 增加全局延迟因子
                    # 'session_log': 'session.log',  # 启用会话日志
                    # 'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)

        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return






























if __name__ == '__main__':
    from pprint import pprint
    # -------------------命令-------------------
    show_cmd = "show ip interface brief"
    # show_cmd = "show interface"
    # show_cmd = 'show version'

    # -------------------控制textfsm-------------------
    # textfsm = False
    textfsm = True

    # ----------------------ssh------------------------
    raw_result = netmiko_show_cred(device_ip,
                                   username,
                                   password,
                                   show_cmd,
                                   'cisco_ios',
                                   use_textfsm=textfsm
                                   )
    if textfsm:
        pprint(raw_result)
    else:
        print(raw_result)
