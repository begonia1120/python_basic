# interfaces = ['loop13']
# cmds = []
# for iface in interfaces:
#             cmds.append(f'interface {iface}')                                          # 追加: interface {接口名}
#             cmds.append(f'ip address {iface} {iface}')                      # 追加: ip address {IP} {掩码}
#             # cmds.append(f'description {iface.description}') if iface.description else None  # 如果有 description，追加: description {描述}
#             # cmds.append(f'no shutdown' if iface.status else 'shutdown')                     # 根据 status 追加 'no shutdown' 或 'shutdown'
#             print(cmds)
#             break

import sqlite3
print(sqlite3.sqlite_version)