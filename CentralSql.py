from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from Task.settings import DB_SETTINGS, logging
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Domain(Base):

    __tablename__ = 'domain'

    id      = Column(Integer, primary_key=True)
    name    = Column(String)
    fdstatus= Column(String)
class Source(Base):

    __tablename__ = 'source'
    
    id        = Column(Integer, primary_key=True)
    source    = Column(String)
    statuss   = Column(String)
    domain_id = Column(Integer, ForeignKey('domain.id'))



class CentralSql:
    def __init__(self):
        self.connection = None
        self.engine     = None
        self.Session    = None
        self.session    = None

    def connect(self):
        try:

            self.engine  = create_engine(self.get_database_url())
            self.Session = sessionmaker(bind=self.engine)
            logging.info("MySQL is connected")
            return self.Session()
        
        except Exception as e:

            logging.error("Error while connecting to MySQLAlchemy:", str(e))

    def get_database_url(self):
        return f"mysql+mysqlconnector://{DB_SETTINGS['USER']}:{DB_SETTINGS['PASSWORD']}@{DB_SETTINGS['HOST']}:{DB_SETTINGS['PORT']}/{DB_SETTINGS['DATABASE']}"
