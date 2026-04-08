import argparse,paramiko

def ssh_run(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=username, password=password, timeout=5,
                look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    ssh.close()
    return result

def main():
    parser = argparse.ArgumentParser(description='網絡設備 SSH 命令執行工具')
    parser.add_argument('-i', '--ip', required=True, help='設備的 IP 地址')
    parser.add_argument('-u', '--username', required=True, help='登入用戶名')
    parser.add_argument('-p', '--password', required=True, help='登入密碼')
    parser.add_argument('-c', '--cmd', required=True, help='要執行的命令')
    args = parser.parse_args()
   
    output = ssh_run(args.ip, args.username, args.password, args.cmd)
    print(output)
if __name__ == '__main__':
    main()
