import paramiko
import time

def qytang_multicmd(host, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=username, password=password, timeout=5, 
                look_for_keys=False, allow_agent=False)
    chan = ssh.invoke_shell()
    time.sleep(1)
    #while chan.recv_ready():
    chan.recv(4096)

    if enable:
        chan.send(b'enable\n')
        time.sleep(1)
        chan.send(f'{enable}\n'.encode())
        time.sleep(1)
        chan.recv(4096)

    all_output = ''
    for cmd in cmd_list:
        chan.send(f'{cmd}\n'.encode())
        time.sleep(wait_time)
        output = chan.recv(65535).decode()
        all_output += output
        
        if verbose:
            print(f'--- {cmd} ---')
            print(output)
    ssh.close()
    return all_output

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