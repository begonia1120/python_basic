from sqlalchemy.orm.session import Session


import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///device_inventory.db?check_same_thread=False',
                       echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Device(Base):
    __tablename__ = 'devices'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(64), nullable=False, index=True)
    type        = Column(String(64), nullable=False)
    version     = Column(String(64))
    location    = Column(String(128))
    create_time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return (f"{self.__class__.__name__}(設備名稱: {self.name} | 類型: {self.type} | "
                f"版本: {self.version} | 位置: {self.location} | 入庫時間: {self.create_time})")

if __name__ == '__main__':
    Base.metadata.create_all(engine, checkfirst=True)

    if session.query(Device).count() == 0:
        device_list = [
            {'name':'R1', 'type':'router', 'version':'IOS XE 17.14', 'location':'Beijing-IDC-A'},
            {'name':'R2', 'type':'router', 'version':'IOS XE 17.14', 'location':'Shanghai-IDC-B'},
            {'name':'SW1', 'type':'switch', 'version':'IOS 15.2', 'location':'Beijing-IDC-A'},
            {'name':'SW2', 'type':'switch', 'version':'IOS 15.2', 'location':'Shanghai-IDC-B'},
            {'name':'FW1', 'type':'firewall', 'version':'ASA 9.16', 'location':'Beijing-IDC-A'},
            {'name':'FW2', 'type':'firewall', 'version':'FTD 7.2', 'location':'Shenzhen-IDC-C'}
        ]
        for device in device_list:
            session.add(Device(**device))
        session.commit()
    print(f"[+] 初始設備數據已寫入數據庫")
    first_run = True
    while True:
        if first_run:
            print("\n請輸入查詢選項:")
            print("輸入 1:查詢所有設備")
            print("輸入 2:根據設備名稱查詢")
            print("輸入 3:根據設備類型查詢")
            print("輸入 4:根據機房位置查詢")
            print("輸入 0:退出")
            first_run = False

        while True:
            choice = input("\n請輸入查詢選項: ").strip()
            if choice  in ('0', '1', '2', '3', '4'):
                break
            print("無效的選項，請重新輸入 (0-4) ")

        if choice == '0':
            break
        
        elif choice == '1':
            devices = session.query(Device).all()
            print('\n'.join(str(d) for d in devices) if devices else f'數據庫中沒有設備')
            


        elif choice == '2':
            name = input("請輸入設備名稱: ")
            devices = session.query(Device).filter(Device.name == name).all()
            print('\n'.join(str(d) for d in devices) if devices else f'未找到設備: {name}')
            
        
        elif choice == '3':
            device_type = input("請輸入設備類型 (router/switch/firewall): ")
            devices = session.query(Device).filter(Device.type == device_type).all()
            print('\n'.join(str(d) for d in devices) if devices else f'未找到設備類型: {device_type}')
            

        elif choice == '4':
            keyword = input("請輸入機房位置關鍵詞: ")
            devices = session.query(Device).filter(Device.location.contains(keyword)).all()
            print('\n'.join(str(d) for d in devices) if devices else f'未找到機房位置: {keyword}')