import mysql.connector as sqltor 
from Task.settings import DB_SETTINGS,logging
class CentralSql:
    def Connection():
    
        mycon = sqltor.connect(
            host    =   DB_SETTINGS["HOST"], 
            user    =   DB_SETTINGS["USER"], 
            passwd  =   DB_SETTINGS["PASSWORD"], 
            database=   DB_SETTINGS["DATABASE"]
        )
        
        if mycon.is_connected():
            logging.info("MySQL is connected")
            return mycon
        else:
            logging.error("MySQL not connected in Central")
