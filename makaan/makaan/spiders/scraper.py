import scrapy
from scrapy.crawler import Crawler
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.makaan.com"]
    start_urls = ["https://www.makaan.com/gurgaon-residential-property/rent-property-in-gurgaon-city"]
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    
    rules = (Rule(LinkExtractor(allow="")),)

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers
    }


    def parse(self, response):
        for ur in response.xpath("//a[@data-type='listing-link']"):
            urls = ur.xpath("@href").get()
            yield response.follow(url=urls, callback=self.parse_data)
           
        for page in range(0,10):
            pages = response.xpath("//a[@aria-label='nextPage']/@href").get()
            yield response.follow(url=pages, callback=self.parse)
            sleep(2)
            
        # for loc in response.xpath("//span[@itemprop='addressLocality']/strong"):
        #     loaction = loc.xpath("text()").get()
        #     yield{
        #         "Location":loaction
        #     }
        
    def parse_data(self,response):
        yield{
            "Area & Type" : response.xpath("//h1[@class='type-wrap']/span[@class='type']/text()").get(),
            "Location" : response.xpath("//div[@class='loc-wrap']/span/text()").get(),
            "Rent" : response.xpath("(//span[@class='val']/text())[1]").get(),
            "Security Deposit" : response.xpath("//td[@title='No Deposit']/text()").get(),
            "Description" : response.xpath("//div[@data-type='smallText']/text()").get(),
            "Locality" : response.xpath("//span[@class='ldesc js-desk']/text()").get()
        }