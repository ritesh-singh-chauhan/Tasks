from itemadapter import ItemAdapter
from pymongo import MongoClient
from ProcessCrawler import *
from Task.items import TaskItem,FullDescription
from CentralSql import CentralSql,text
d={}
obj=CentralSql()

class TaskPipeline:
    def process_item(self, item, spider):
        return item
    

class MongoDBPipeline:
    collection_name     = "france_america"
    def __init__(self, mongo_uri, mongo_db):
        self.client     =   MongoClient(mongo_uri)
        self.db         =   self.client[mongo_db]
        self.collection =   self.db[self.collection_name]
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db  = crawler.settings.get('MONGO_DATABASE')
        )
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item,TaskItem):
            link        =   item['link']
            spider_fd   =   spider.name+"_fd"   #-------------------TO dynamically give the name of spider of the full description----------           
            try:

                if spider.name not in d.keys():
                    session=obj.connect()
                    query = text(f"SELECT Domain.fdstatus FROM Source,Domain where Source.domain_id=Domain.id and Domain.name='{spider.name}'")
                    result = session.execute(query)
                    fdstatus=result.fetchall()
                    d[spider.name]=fdstatus[0][0]
                    session.close()
                    logging.info("Status of the FD",fdstatus)

                if d[spider.name]==1:
                    processObj=ProcessCrawler()
                    processObj.feed_fd(spider_fd,link) 
                                       
            except Exception as error:
                logging.error(f"Error Found in SQL Query pipeline:{error}")
            
            finally:
                session.close()

            self.collection.insert_one(item)
        if isinstance(item,FullDescription):
            self.collection.update_one({"link_hash":item['link_hash']},{"$set":{"Full_Description":item['fulldescription']}})
        return item
        
    def close_spider(self, spider):
        self.client.close()