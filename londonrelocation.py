import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from property import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonspider'
    page = 1
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        items = Property()

        title = response.css(".h4-space a::text").extract()
        price = response.css("h5::text").extract()
        url = response.css(".h4-space a::href").extract()

        items['title'] = title
        items['price'] = price
        items['url'] = url

        yield items

        next_page = response.css('.fa-angle-right a::href')
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)




        # an example for adding a property to the json list:
        # property = ItemLoader(item=Property())
        # property.add_value('title', '2 bedroom flat for rental')
        # property.add_value('price', '1680') # 420 per week
        # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        # return property.load_item()
