intf1 = "Gi0/0"
status1 = "up"
speed1 = "1G"

intf2 = "Gi0/1"
status2 = "down"
speed2 = "1G"

intf3 = "Gi0/2"
status3 = "up"
speed3 = "10G"

row_fmt = "{:<10}{:<8}{}"

print(row_fmt.format("接口", "狀態", "速率"))
print("--------------------------------")
print(row_fmt.format(intf1, status1, speed1))
print(row_fmt.format(intf2, status2, speed2))
print(row_fmt.format(intf3, status3, speed3))