from itemadapter import ItemAdapter
from pymongo import MongoClient
from ProcessCrawler import *
from Task.items import TaskItem,FullDescription
from CentralSql import CentralSql,Domain,Source
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
        logging.info("Step-8 The Engine sends processed items to Item Pipelines, then send processed Requests to the Scheduler and asks for possible next Requests to crawl.")
        if isinstance(item,TaskItem):
            link        =   item['link']
            spider_fd   =   spider.name+"_fd"   
            try:

                if spider.name not in d.keys():
                    session     =    obj.connect()    
                    query       =   session.query(Domain.fdstatus).join(Source, Source.domain_id == Domain.id).filter( Domain.name == spider.name )
    
                    fdstatus    =   query.all()
                    d[spider.name]= fdstatus[0][0]
                    session.close()
                    logging.info("Status of the FD",fdstatus)

                if d[spider.name]   ==  1:
                    processObj  =   ProcessCrawler()
                    processObj.feed_fd(spider_fd,link) 
                                       
            except Exception as error:
                logging.error(f"Error Found in SQL Query pipeline:{error}")
            
            self.collection.insert_one(dict(item))
        if isinstance(item,FullDescription):
            self.collection.update_one({"link_hash":item['link_hash']},{"$set":{"Full_Description":item['fulldescription']}})
        #return item 
        
    def close_spider(self, spider):
        self.client.close()