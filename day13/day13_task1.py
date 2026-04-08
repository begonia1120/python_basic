import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day12.day12_task1 import qytang_multicmd

class Interface:
    """接口配置类，只保存接口数据"""
    def __init__(self, name):
        self.name = name
        self.device = None      # 所属设备，默认未绑定
        self.ip_address = ''    # IP 地址，默认空字符串
        self.mask = ''          # 子网掩码，默认空字符串
        self.description = ''   # 接口描述，默认空字符串
        self.status = False     # True=no shutdown, False=shutdown，默认关闭
 
    def __str__(self):
        """格式化打印接口信息"""
        status_str = 'no shoutdown' if self.status else 'shutdown'  # 如果 self.status 为 True 则为 'no shutdown'，否则为 'shutdown'
        device_ip = self.device.ip if self.device else '未綁定設備'  # 如果 self.device 存在则取 self.device.ip，否则显示 '未绑定设备'
        lines = [
            f"接口名称    : {self.name}",
            f"所属设备    : {device_ip}",
            f"IP 地址     : {self.ip_address} {self.mask}",
            f"描述        : {self.description}",
            f"状态        : {status_str}",
        ]
        return '\n'.join(lines)

class NetworkDevice:
    """网络设备类，保存设备登录信息及关联的接口"""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.interfaces = []

    def add_interface(self, interface):
        """将接口加入本设备，并建立双向关联"""
        interface.device = self           # 把 interface 的 device 属性指向自己（self）
        self.interfaces.append(interface)  # 把 interface 追加到 self.interfaces 列表

    def apply(self):
        """将所有关联接口的配置一次性下发到设备"""
        if not self.interfaces:
            print(f"[*] {self.ip} 没有待下发的接口配置")
            return

        cmds = ['config ter']
        for iface in self.interfaces:
            cmds.append(f'interface {iface.name}')                                          # 追加: interface {接口名}
            cmds.append(f'ip address {iface.ip_address} {iface.mask}')                      # 追加: ip address {IP} {掩码}
            cmds.append(f'description {iface.description}') if iface.description else None  # 如果有 description，追加: description {描述}
            cmds.append(f'no shutdown' if iface.status else 'shutdown')                     # 根据 status 追加 'no shutdown' 或 'shutdown'
        cmds.append('end')

        iface_names = ', '.join(iface.name for iface in self.interfaces)
        print(f"[*] 正在 {self.ip} 上批量应用接口配置: {iface_names}")
        qytang_multicmd(self.ip, self.username, self.password, cmds, verbose=False)
        print(f"[*] {self.ip} 所有接口配置应用完成！")

    def __str__(self):
        """打印设备信息及下属接口列表"""
        lines = [
            f"设备 IP      : {self.ip}",
            f"用户名       : {self.username}",
            "接口列表     :",
        ]
        if not self.interfaces:
            lines.append("  （无）")
        else:
            for iface in self.interfaces:
                status_str = 'no shutdown' if iface.status else 'shutdown'
                lines.append(f"  - {iface.name}: {iface.ip_address} {iface.mask}, {status_str}")
        return '\n'.join(lines)

if __name__ == '__main__':
    r1 = NetworkDevice('10.10.1.1', 'admin', 'Cisc0123')
    
    # 創建第一個接口並設置參數
    loop13 = Interface('Loopback13')
    loop13.ip_address = '13.13.13.13'
    loop13.mask = '255.255.255.255'
    loop13.description = 'Created_by_Python'
    loop13.status = True
    r1.add_interface(loop13)
    print(loop13)

    #創建第二個接口並設置參數
    gi2 = Interface('GigabitEthernet2')
    gi2.ip_address = '172.16.1.12'
    gi2.mask = '255.255.255.0'
    gi2.description = 'Created_by_Python'
    gi2.status = True
    r1.add_interface(gi2)
    print(r1)
    r1.apply()