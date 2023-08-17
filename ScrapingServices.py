from ProcessCrawler import *
from redis import Redis
from rq import Queue
from CentralSql import CentralSql,Source,Domain
from Task.settings import REDIS_SETTINGS,logging,CUSTOM_CURRENT_TIME 
# import os
# import sys
# from pathlib import Path
# central=Path(__file__).resolve()
# processcrawler=os.path.join(central.parent,"Task/pipelines")
# print(sys.path)
# sys.path.insert(0,str(processcrawler))
# print(sys.path)

obj = CentralSql()

class ScrapingServices:

    def __init__(self):
        self.session   =    obj.connect()

    def UsingRedis(self):
        try:
            logging.info(CUSTOM_CURRENT_TIME)
            query = self.session.query(Domain.name, Source.source, Source.statuss)\
               .join(Source, Source.domain_id == Domain.id)\
               .filter(Domain.id > 5)
            
            rows = query.all()
    
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