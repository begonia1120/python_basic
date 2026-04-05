import re
port_list = ['eth 1/101/1/42','eth 1/101/1/26','eth 1/101/1/23','eth 1/101/1/7','eth 1/101/2/46','eth 1/101/1/34',\
    'eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

#port_list.sort(key=lambda x: (int(re.match(r'^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).group(3)),int(re.match(r'^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).group(4))))
result = sorted(port_list, key=lambda x: (int(re.match(r'^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).group(3)),int(re.match(r'^eth (\d)/(\d\d\d)/(\d)/(\d+)', x).group(4))))
print(port_list)
print(result)

# 第二種方法參考
# pattern = re.compile(r'^eth (\d)/(\d\d\d)/(\d)/(\d+)')
# port_list.sort(key=lambda x: (int(pattern.match(x).group(3)),int(pattern.match(x).group(4))))
# print(port_list)