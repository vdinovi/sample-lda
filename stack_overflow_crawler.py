import scrapy

class StackOverflowCrawler(scrapy.Spider):
    name = 'question'
    download_delay = 2
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        # follow question links
        for href in response.xpath("//div[@class='question-summary']/div[@class='summary']/h3/a/@href"):
           yield response.follow(href, self.parse_question)

        # follow pagination
        for href in response.xpath("//div[@class='pager fl']/a[@rel='next']/@href"):
            yield response.follow(href, self.parse)

    def parse_question(self, response):
        with open('data.txt', 'a') as f:
            f.write(''.join(response.css('.post-text p::text').extract()))

