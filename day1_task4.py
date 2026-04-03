import random
octet1 = random.randint(0, 255)
octet2 = random.randint(0, 255)
octet3 = random.randint(0, 255)
octet4 = random.randint(0, 255)

ip_address = str(octet1) + "." + str(octet2) + "." + str(octet3) + "." + str(octet4)
print("隨機產生的IPv4地址為: " + ip_address)