interface = "GigabitEthernet0/0/1"

intf_type = interface[:15]
intf_num = interface[15:]

print("接口類型: " + intf_type)
print("接口編號: " + intf_num)