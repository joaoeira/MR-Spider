import scrapy
import re

class AmazonLinksSpider(scrapy.Spider):
    name = "amazon"

    def start_requests(self):
        url = 'https://marginalrevolution.com/marginalrevolution/2014/04/ancient-religions-modern-politics.html/'

        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):
        for amazonlink in response.css(".entry-content").re(r'http://www.amazon.com/.*'):
            print(re.search('.+?(?=ref=)',amazonlink).group(0))
            