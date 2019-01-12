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
    start_urls = ('https://healthyceleb.com/category/statistics/sports-stars/male-sports-stars/page/1',)


    def parse(self, response):
        for i in range(2,6):
            temp = self.start_urls[0]
            nlink = temp.split()[0]
            newlink = nlink[:-1] + str(i),
            self.start_urls = self.start_urls + newlink
            yield scrapy.Request(newlink[0], callback = self.Nparse)

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
        w = item['id']
        
        item['Name'] = response.xpath('//*/strong[contains(text(),"Quick Info")]/text()').extract_first().replace("Quick Info", "")
        
        item['Gender'] = response.xpath('//*[@id="td-outer-wrap"]/div[2]/div/div[1]/div/span[3]/a/text()').extract()
        
        item['Height'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"cm")]/text()').extract_first().split("or")[1].replace("cm", "")
        
        #item['Weight'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"kg")]/text()').extract_first().split("or")[0].replace("kg", "")
        item['Weight'] = response.xpath('//*[@id="post-'+str(w)+'"]/div[3]/table/tbody/tr[2]/td[2]/text()').extract_first().replace("kg", "")

        item['url'] = response.url
        yield item