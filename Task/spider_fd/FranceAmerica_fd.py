
from Task.spiders.Central import Centralfd
from Task.items import FullDescription
import hashlib
from w3lib.html import remove_tags
import html
from Task.settings import logging
class FranceAmerica_fd(Centralfd):

    name="franceamerica_fd"

    def parse(self,response):
        
        item    =   FullDescription()
        response.selector.remove_namespaces()
        st      =   remove_tags("\n".join(response.xpath("//div[@class='elementor-section-wrap']//h2 | //div[@class='elementor-section-wrap']//p").getall()))
        result  =   hashlib.md5(self.url.encode())

        try:
            item['link_hash']       =   result.hexdigest()

        except:
            item['link_hash']       =   ''

        try:
            item['fulldescription'] =   html.unescape(st)

        except:
            item['fulldescription'] =   ""


        yield item