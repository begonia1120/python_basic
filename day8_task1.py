import os
import time

while True:
    output = os.popen('ss -tulnp').read()
    found = False
    for line in output.splitlines():
        if 'tcp' in line and ':80 ' in line:
            found = True
            break
    if found:
        print('[!] 告警: TCP/80 已開放! 請檢查是否為授權服務。 ')
        break
    else:
        print('[*] 檢測中... TCP/80未開放')
    time.sleep(1)