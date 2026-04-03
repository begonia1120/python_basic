device1_name = "CoreSwitch"
device1_ip = "10.1.1.1"
device1_role = "核心交換機"

device2_name = "Firewall"
device2_ip = "10.1.1.2"
device2_role = "防火牆"

device3_name = "WLC"
device3_ip = "10.1.1.3"
device3_role = "無線控制器"

print("========== IP地址規劃表 ==========")
row_fmt = "{:<16}{:<16}{}"
print(row_fmt.format("設備名稱", "管理地址", "角色"))
print("-----------------------------------------")
print(row_fmt.format(device1_name, device1_ip, device1_role))
print(row_fmt.format(device2_name, device2_ip, device2_role))
print(row_fmt.format(device3_name, device3_ip, device3_role))
print("=========================================")