import re
import os

route_n_result = os.popen("route -n").read()
pattern = r'0\.0\.0\.0\s+([\d.]+)\s+0\.0\.0\.0\s+UG'
match = re.search(pattern, route_n_result)
gateway = match.group(1)

print("網關為: " + gateway)