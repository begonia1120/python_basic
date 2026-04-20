import socket,sys,struct,hashlib,pickle

address = ('0.0.0.0', 6666)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)

print('UDP服務器就緒!等待戶數據!')
while True:
    try:
        recv_source_data = s.recvfrom(512)
        rdata, addr = recv_source_data
        header = rdata[:16]

        uppack_header = struct.unpack('>HHLQ', header)
        version = uppack_header[0]
        pkt_type = uppack_header[1]
        seq_id = uppack_header[2]
        length = uppack_header[3]

        rdata = rdata[16:]
        data = rdata[:length]
        md5_recv = rdata[length:]

        m = hashlib.md5()
        m.update(header + data)
        md5_value = m.digest()

        if md5_recv == md5_value:
            print('=' * 80)
            print(f'{"數據源自於":<30}:{str(addr):<30}')
            print(f'{"數據序列號":<30}:{seq_id:<30}')
            print(f'{"數據長度為":<30}:{length:<30}')
            print(f'{"數據內容為":<30}:{str(pickle.loads(data))}')
        else:
            print('MD5校驗錯誤! ')
    except KeyboardInterrupt:
        sys.exit()
