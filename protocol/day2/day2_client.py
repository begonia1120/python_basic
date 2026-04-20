import socket,struct,hashlib,pickle

def udp_send_data(ip, port, data_list):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    version = 1
    pkt_type = 1
    seq_id =1
    max_payload = 512
    try:
        for x in data_list:
            send_data = pickle.dumps(x)
            if len(send_data) > max_payload:
                raise ValueError(f'seq_id={seq_id} 資料長度 {len(send_data)} 超過上限 {max_payload} bytes')
            header = struct.pack('>HHLQ', version, pkt_type, seq_id, len(send_data))
            m = hashlib.md5()
            m.update(header + send_data)
            md5_value = m.digest()
            s.sendto(header + send_data + md5_value, address)
            seq_id +=1
    finally:
        s.close()

if __name__ == '__main__':
    from datetime import datetime
    user_data = ['乾頤堂', [1, 'qytang', 3], {'qytang': 1, 'test': 3}, {'datetime': datetime.now()}]
    # user_data = ['A' * 600]
    try:
        udp_send_data("10.10.1.200", 6666, user_data)
    except ValueError as e:
        print(f"預期的例外：{e}")