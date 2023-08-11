from itemadapter import ItemAdapter
from pymongo import MongoClient
from ProcessCrawler import *
from Task.items import TaskItem,FullDescription
from CentralSql import CentralSql
d={}
mycon=CentralSql.Connection()
class TaskPipeline:
    def process_item(self, item, spider):
        return item
class MongoDBPipeline:
    collection_name = "FranceAmerica"
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )
    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def process_item(self, item, spider):
        if isinstance(item,TaskItem):
            link=item['link']
            spider_fd=spider.name+"_fd"   #-------------------TO dynamically give the name of spider of the full description----------           
            try:

                if spider.name not in d.keys():
                    cursor=mycon.cursor()
                    cursor.execute(f"SELECT Domain.fdstatus FROM Source,Domain where Source.domain_id=Domain.id and Domain.name='{spider.name}'")
                    FdStatus=cursor.fetchall()
                    d[spider.name]=FdStatus[0][0]
                    logging.info("Status of the FD",FdStatus)

                if d[spider.name]==1:
                    processObj=ProcessCrawler()
                    processObj.feed_fd(spider_fd,link)                    
            except Exception as error:
                logging.error(f"Error Found in SQL Query pipeline:{error}")


            self.collection.insert_one(dict(item))
        if isinstance(item,FullDescription):
            self.collection.update_one({"link_hash":item['link_hash']},{"$set":{"Full_Description":item['fulldescription']}})
        return item
        
    def close_spider(self, spider):
        self.client.close()
