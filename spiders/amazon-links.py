import scrapy
import re

class AmazonLinksSpider(scrapy.Spider):
    name = "amazon"

    def start_requests(self):
        urls = ['https://marginalrevolution.com/marginalrevolution/2018/12/what-ive-been-reading-132.html',
                'https://marginalrevolution.com/marginalrevolution/2018/11/what-ive-been-reading-131.html']

        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):

        title = response.css(".entry-title::text").extract()[0]

        links = []
        for amazonlink in response.css(".entry-content").re(r'https://www.amazon.com/.*'):
            links.append(re.search('.+?(?=ref=)',amazonlink).group(0))
            
        yield {
            'url': response.request.url,
            'title': title,
            'links': links
        }
        