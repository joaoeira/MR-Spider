import scrapy
import re

class AmazonLinksSpider(scrapy.Spider):
    name = "amazon"

    custom_settings = {
        "USER_AGENT": "*"
    }
    handle_httpstatus_list = [301]
    def start_requests(self):
        url = 'https://marginalrevolution.com/marginalrevolution/2018/12/sunday-assorted-links-194.html'

        filename_archive = 'mr-links-mined.txt'
        archive = open(filename_archive, 'a')    
        archive.write(url) 
        archive.close()

        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):

        title = response.css(".entry-title::text").extract()[0]
        date = response.css(".entry-date::text").extract()[0]
        title_post = response.css(".entry-title::text").extract()[0]

        links = []
        if(response.css(".entry-content").re('https://www.amazon.com/.*')):
            for amazonlink in response.css(".entry-content").re('https://www.amazon.com/.*'):
                links.append(re.search('.+?(?=ref=)',amazonlink).group(0))
        elif(response.css(".entry-content").re('http://www.amazon.com/.*')):
            for amazonlink in response.css(".entry-content").re('http://www.amazon.com/.*'):
                links.append(re.search('.+?(?=ref=)',amazonlink).group(0))

        if links:    
            yield {
                'title-post': title_post,
                'date': date,
                'url': response.request.url,
                'title-book': title,
                'links': links
            }
        # else:
        #     yield {
        #         'title-post': title_post,
        #         'date': date,
        #         'status': "NONE"
        #     }

        filename_links = 'mr-links1.txt'
        with open(filename_links, 'r') as f:
            mrlinks = f.readlines()
        filename_archive = 'mr-links-mined7.txt'
 
        archive = open(filename_archive, 'a')        

        for mrlink in mrlinks:
            archive.write(mrlink)
            yield scrapy.Request(mrlink.strip(),callback=self.parse)
        
        with open(filename_links, 'w') as f:
            f.close()            

        