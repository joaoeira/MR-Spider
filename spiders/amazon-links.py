import scrapy
import re

class AmazonLinksSpider(scrapy.Spider):
    name = "amazon"

    custom_settings = {
        'DOWNLOAD_DELAY': '1.0',
        "USER_AGENT": "*"
    }
    handle_httpstatus_list = [301]
    def start_requests(self):
        url = 'https://marginalrevolution.com/marginalrevolution/2018/12/sunday-assorted-links-194.html'

        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):

        title = response.css(".entry-title::text").extract()[0]

        links = []
        for amazonlink in response.css(".entry-content").re(r'https://www.amazon.com/.*'):
            links.append(re.search('.+?(?=ref=)',amazonlink).group(0))

        if links:    
            yield {
                'url': response.request.url,
                'title': title,
                'links': links
            }

        filename = 'mr-links.txt'
        with open(filename, 'r') as f:
            mrlinks = f.readlines()
            for mrlink in mrlinks:
                yield scrapy.Request(mrlink.strip(),callback=self.parse)