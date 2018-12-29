import scrapy

pagenumber = 1

class MRLinksSpider(scrapy.Spider):
    name = "mr"

    custom_settings = {
        'DOWNLOAD_DELAY': '2.0',
        "USER_AGENT": "*"
    }
    handle_httpstatus_list = [301]
    def start_requests(self):
        url = 'https://marginalrevolution.com/page/1'

        yield scrapy.Request(url=url,callback=self.parse)

    def parse(self,response):

        links = response.css('.entry-title a::attr(href)').extract()
        print(response)
        if not links:
            self.log('no links')
            exit()
        
        filename = 'mr-links.txt'
        with open(filename, 'a') as f:
            for item in links:
                f.write(item+'\n')
            self.log('Saved file with links')


        currenturl = response.request.url

        if currenturl == 'https://marginalrevolution.com/':
            self.log("THERE WAS A 301 ERROR")
            self.log("SHUTTING DOWN SPIDER")
            exit()

        elif currenturl[36:] != '1800':
            print(currenturl)
            next_page = currenturl[:36] + str(int(currenturl[36:])+1)
            yield scrapy.Request(next_page,callback=self.parse)

        