import mysql.connector as sqltor
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from Task.settings import DB_SETTINGS, logging
from sqlalchemy import text


class CentralSql:
    def __init__(self):
        self.connection = None
        self.engine = None
        self.Session = None
        self.session = None

    def connect(self):
        try:
            self.connection = sqltor.connect(
                host=DB_SETTINGS["HOST"], 
                user=DB_SETTINGS["USER"], 
                passwd=DB_SETTINGS["PASSWORD"], 
                database=DB_SETTINGS["DATABASE"],
                port=DB_SETTINGS["PORT"]
            )
            if self.connection.is_connected():
                print("MySQL is connected")
                self.engine = create_engine(self.get_database_url())
                self.Session = sessionmaker(bind=self.engine)
                return self.Session()
            else:
                logging.error("MySQL not connected in Central")
            
        
        except Exception as e:
            logging.error("Error while connecting to MySQL:", str(e))

    def get_database_url(self):
        return f"mysql+mysqlconnector://{DB_SETTINGS['USER']}:{DB_SETTINGS['PASSWORD']}@{DB_SETTINGS['HOST']}:{DB_SETTINGS['PORT']}/{DB_SETTINGS['DATABASE']}"
