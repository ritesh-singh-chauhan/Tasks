from ProcessCrawler import *
from redis import Redis
from rq import Queue
from CentralSql import CentralSql,text
from Task.settings import REDIS_SETTINGS,logging
obj=CentralSql()
class ScrapingServices:

    def __init__(self):
        self.session   =    obj.connect()

    def UsingRedis(self):
        try:
            print(self.session)
            query = text("SELECT Domain.name, Source.source, Source.statuss FROM Source, Domain where Source.domain_id=Domain.id and Domain.id>5")
            result = self.session.execute(query)
            rows = result.fetchall()
    
            for row in rows:
                print(row)
            
            redis_conn = Redis(
                host    =   REDIS_SETTINGS["REDIS_HOST"], 
                port    =   REDIS_SETTINGS["REDIS_PORT"], 
                db      =   REDIS_SETTINGS["REDIS_DB"]
            )

            try:
                redis_conn.ping()
                logging.info('Redis connected Successfully')

            except Exception as redis_error:
                logging.error(f"Error while checking Redis connection: {redis_error}")
            q = Queue(connection=redis_conn)
            for row in rows:
                spidername,sourcelink,status= row[0], row[1], row[2]
                if status == 1:
                    processObj=ProcessCrawler()
                    print(q.enqueue(processObj.feeds, args=(spidername,sourcelink)))
                    
        except Exception as error:
            logging.error(f"Error found in ScrapingServices{error}")

        finally:
            self.session.close()

obj_scraping=ScrapingServices()
obj_scraping.UsingRedis()