import paramiko
import re

def ssh_run(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=22, username=username, password=password, timeout=5, 
                look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    ssh.close()
    return result

if __name__ == '__main__':
    output = ssh_run('10.10.1.200', 'root', 'Jackal1120', 'route -n')
    for line in output.splitlines():
        match = re.match(r'0\.0\.0\.0\s+([\d.]+)\s+0\.0\.0\.0\s+UG', line)
        if match:
            print(f'默認網關: {match.group(1)}')
            break