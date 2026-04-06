import paramiko
import time

def qytang_multicmd(host, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=username, password=password, timeout=5, 
                look_for_keys=False, allow_agent=False)
    chan = ssh.invoke_shell()
    time.sleep(1)
    while chan.recv_ready():
        chan.recv(4096)
    
    for cmd in cmd_list:
        chan.send(cmd + '\n')
        time.sleep(wait_time)
        if verbose:
            output = ''
            while chan.recv_ready():
                output += chan.recv(2048).decode()
            print(f'\n--- {cmd} ---\n{output}')
    ssh.close()

if __name__ == '__main__':
    cmd_list = [
        'terminal length 0',
        'show version',
        'config ter',
        'router ospf 1',
        'network 10.0.0.0 0.0.0.255 area 0',
        'end',
    ]
    qytang_multicmd('10.10.1.1', 'admin', 'Cisc0123', cmd_list)