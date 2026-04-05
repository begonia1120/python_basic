from readline import replace_history_item
from pythonping import ping

def ping_check(host, count=1, timeout=2):
    result = ping(host, count=count, timeout=timeout)
    if result.success():
        return True, result.rtt_avg_ms
    else:
        return False, None

if __name__ == '__main__':
    gateways = ['196.21.5.1', '10.0.0.1', '172.16.1.1', '8.8.8.8']

    for gw in gateways:
        reachable, rtt = ping_check(gw)
        if reachable:
            print(f'{gw:<13}: 可達   | RTT: {rtt:.2f} ms')
        else:
            print(f'{gw:<13}: 不可達')