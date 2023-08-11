import scrapy

class Central(scrapy.Spider):

    def __init__(self,url=None, **kwargs):

        self.url=url
        super().__init__(url=self.url)
    
    def start_requests(self):
        for url in self.url:
            yield scrapy.Request(url=self.url, callback=self.parse,
                           headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
                           )
     
            
class Centralfd(scrapy.Spider):

    def __init__(self, url=None, **kwargs):

        self.url=url
        super().__init__(url=self.url, **kwargs)

    def start_requests(self):   
        yield scrapy.Request(url=self.url, callback=self.parse,
                           headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}                             
                           )
    