import sys, os, hashlib, time, datetime, re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from day12.day12_task1 import qytang_multicmd

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///router_config.db',
                       connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)

class RouterConfig(Base):
    __tablename__ = 'router_config'
    id            = Column(Integer, primary_key=True)
    router_ip     = Column(String(64),    nullable=False, index=True)
    router_config = Column(String(99999), nullable=False)
    config_hash   = Column(String(500),   nullable=False)
    record_time   = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'路由器IP地址: {self.router_ip} | '
                f'配置Hash: {self.config_hash} | '
                f'紀錄時間: {self.record_time})')
Base.metadata.create_all(engine, checkfirst=True)

def get_show_run(host, username, password):
    raw = qytang_multicmd(host, username, password,
                          ['terminal length 0', 'show running-config'], verbose=False)
    match = re.search(r'(hostname[\s\S]+end)', raw)
    config = match.group(1)
    config_hash = hashlib.sha256(config.encode('utf-8')).hexdigest()
    return config, config_hash

def save_config(host, config, config_hash):
    with Session() as session:
        record = RouterConfig(router_ip=host, router_config=config, config_hash=config_hash)
        session.add(record)
        session.commit()

def get_latest_two_hashes(host):
    with Session() as session:
        results = (session.query(RouterConfig)
        .filter(RouterConfig.router_ip == host)
        .order_by(RouterConfig.id.desc())
        .limit(2)
        .all())
    return results

if __name__ == '__main__':
    host     = '10.10.1.1'
    username = 'admin'
    password = 'Cisc0123'

    print(f'[*] 開始監控 {host} 的配置變化，每 5 秒採集一次...\n')
    try:
        while True:
            config, config_hash = get_show_run(host, username, password)
            save_config(host, config, config_hash)
            records = get_latest_two_hashes(host)

            if len(records) < 2:
                print(f'本次採集的HASH:{config_hash}')
            elif records[0].config_hash == records[1].config_hash:
                print(f'本次採集的HASH:{config_hash}')
            else:
                print(f'==========配置發生變化==========')
                print(f'{"  THE MOST RECENT HASH":<25}{records[0].config_hash}')
                print(f'{"  THE LAST HASH":<25}{records[1].config_hash}')
            time.sleep(5)
    except KeyboardInterrupt:
        print(f'\n\n[!] 收到停止信號，停止監控 {host} 的配置變化...')