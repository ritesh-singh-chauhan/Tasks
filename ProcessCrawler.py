from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Task.settings import logging
class ProcessCrawler:
    def feeds(self,spidername,sourcelink):
        self.process = CrawlerProcess(get_project_settings())
        self.process.crawl(spidername,sourcelink)
        self.process.start()
    
    def feed_fd(self,spider_fd,url):
        self.url=url
        try:
            process = CrawlerProcess(get_project_settings())
            process.crawl(spider_fd,self.url)
            process.start()
        except Exception as error:
            logging.error(f"Error found in full description :{error}")