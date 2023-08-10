from ProcessCrawler import *
from redis import Redis
from rq import Queue
from CentralSql import CentralSql
from Task.settings import REDIS_SETTINGS,logging
class ScrapingServices:

    def UsingRedis(self):
        mycon= CentralSql.Connection()
        try:
            cursor=mycon.cursor()
            cursor.execute("SELECT Domain.name, Source.source, Source.statuss FROM Source, Domain where Source.domain_id=Domain.id and Domain.id>5") #source status must be 1 to crawl spider
            Datasql= cursor.fetchall()
            redis_conn = Redis(host=REDIS_SETTINGS["redis_host"], port=REDIS_SETTINGS["redis_port"], db=REDIS_SETTINGS["redis_db"]) #using default db=0
            try:
                redis_conn.ping()
                logging.info('Redis connected Successfully')

            except Exception as redis_error:
                logging.error(f"Error while checking Redis connection: {redis_error}")
            q = Queue(connection=redis_conn)
            for row in Datasql:
                spidername,sourcelink,status= row[0], row[1], row[2]
                if status == 1:
                    processObj=ProcessCrawler()
                    print(q.enqueue(processObj.feeds, args=(spidername,sourcelink)))
                    
        except Exception as error:
            logging.error(f"Error found in ScrapingServices{error}")

        finally:
            cursor.close()

obj_scraping=ScrapingServices()
obj_scraping.UsingRedis()