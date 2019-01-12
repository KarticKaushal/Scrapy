import scrapy
from scrapy.item import Item, Field
from scrapy.http import Response

class MalesItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    Name = scrapy.Field()
    Gender = scrapy.Field()
    Height = scrapy.Field()
    Weight = scrapy.Field()
    url = scrapy.Field()
    pass


class Males(scrapy.Spider):
    name = "males"
    allowed_domains = ["healthyceleb.com"]
    start_urls = ('https://healthyceleb.com/category/statistics/sports-stars/male-sports-stars/',)


    def parse(self, response):
        for i in range(1,5):
            newlink = response.xpath('/html/head/link['+str('i')]')
            newlink = response.urljoin(i)
             
            print(newlink)
            yield scrapy.Request(newlink, callback = self.Nparse)


    def Nparse (self, response):
        links = response.xpath('//*[@class="td-ss-main-content"]//h3/a/@href').extract()
        print(links)
        for link in links:
            abs_url = response.urljoin(link)
            yield scrapy.Request(abs_url, callback = self.parse_indetail)

    def parse_indetail(self, response):
        item = MalesItem()
        item['id'] = response.url.split("/")[-1]
        print(item['id'])
        
        item['Name'] = response.xpath('//*/strong[contains(text(),"Quick Info")]/text()').extract_first().replace("Quick Info", "")
        
        item['Gender'] = response.xpath('//*[@id="td-outer-wrap"]/div[2]/div/div[1]/div/span[3]/a/text()').extract()
        
        item['Height'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"cm")]/text()').extract_first().split("or")[1].replace("cm", "")
        
        item['Weight'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"kg")]/text()').extract_first().split("or")[0].replace("kg", "")

        item['url'] = response.url
        yield item