version_raw = "    Cisco IOS XE Software, Version 17.03.04    "

version_stripped = version_raw.strip()
version_upper = version_stripped.upper()
version_replaced = version_upper.replace("17.03.04", "17.06.01")

print("去掉空格: " + version_stripped)
print("轉為大寫: " + version_upper)
print("替換版本: " + version_replaced)