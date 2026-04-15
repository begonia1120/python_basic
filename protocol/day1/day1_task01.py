import logging,sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *
from protocol.tools.get_mac_netifaces import get_mac_address
from protocol.tools.scapy_iface import scapy_iface

def gratuitous_arp(ip_address, iface):
    localmac = get_mac_address(iface)
    gratuitous_arp_pkt = Ether(src=localmac,
                               dst='ff:ff:ff:ff:ff:ff') / ARP(op=2,
                                                              hwsrc=localmac,
                                                              hwdst=localmac,
                                                              psrc=ip_address,
                                                              pdst=ip_address)
    sendp(gratuitous_arp_pkt, iface=scapy_iface(iface), verbose=False)

if __name__ == '__main__':
    gratuitous_arp('10.10.1.1', iface='ens224')





# from tabnanny import verbose
# import logging,time
# logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

# from scapy.all import ARP, Ether, sr1, sendp

# def arp_request(ip_address, my_mac, iface='ens224'):
#     try:
#         while True:
#             ether_layer = Ether(dst='ff:ff:ff:ff:ff:ff')
#             arp_layer = ARP(op=2,
#                             psrc=ip_address,
#                             hwsrc=my_mac,
#                             pdst=ip_address,
#                             hwdst='ff:ff:ff:ff:ff:ff')
#             sendp(ether_layer / arp_layer, iface=iface, verbose=False)
#             time.sleep(3)
#             #return ip_address, gratuitous.getlayer(ARP).fields.get('hwsrc')
#     except KeyboardInterrupt:
#         print('\n[!] 接收到停止信號，已停止執行')

# if __name__ == '__main__':
#     ip_address = '10.10.1.1'
#     my_mac     ='00:0c:29:e5:ee:6c'
#     iface      ='ens224'
#     arp_request(ip_address, my_mac, iface)