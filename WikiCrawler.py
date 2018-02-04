import scrapy

class WikiCrawler(scrapy.Spider):
    name = 'WikiCrawler'
    download_delay = 2
    start_urls = ['https://en.wikipedia.org/wiki/Child_care']
    crawled = []

    def parse(self, response):
        print('RESPONSE')
        for p in response.css('div.mw-body-content p'):
            # here's all of the content
            with open('master.txt', 'a') as f:
                f.write('\n')
                f.write(''.join(p.extract()))
            for a in p.css('a::attr(href)'):
                # got all of the links
                link = 'https://en.wikipedia.org' + a.extract()
                if link not in self.crawled:
                    self.crawled.append(link)
                    yield response.follow(link, callback=self.parse)
