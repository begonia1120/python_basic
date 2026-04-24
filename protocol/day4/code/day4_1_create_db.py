from sqlalchemy.orm.session import Session
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:////python_basic/protocol/day4/code/sqlalchemy_syslog_sqlite3.db?check_same_thread=False',
                       echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class RouterMonitor(Base):
    __tablename__ = 'router_monitor'

    id                 = Column(Integer, primary_key=True)
    device_ip          = Column(String(64), nullable=False)
    cpu_useage_percent = Column(Integer, nullable=False)
    mem_use            = Column(Integer, nullable=False)
    mem_free           = Column(Integer, nullable=False)
    record_datetime    = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)


    def __repr__(self):
        return f'{self.__class__.__name__}(Router: {self.device_ip} ' \
               f'| Datetime: {self.record_time} ' \
               f'| CPU_Usage_Percent: {self.cpu_useage_percent} ' \
               f'| MEM Use: {self.mem_use} ' \
               f'| MEM Free: {self.mem_free})'

if __name__ == "__main__":
    Base.metadata.create_all(engine, checkfirst=True)