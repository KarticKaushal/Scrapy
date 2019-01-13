import scrapy
from scrapy.item import Item, Field
from scrapy.http import Response

class FemalesItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    Name = scrapy.Field()
    Gender = scrapy.Field()
    Height = scrapy.Field()
    Weight = scrapy.Field()
    url = scrapy.Field()
    pass


class Females(scrapy.Spider):
    name = "females"
    allowed_domains = ["healthyceleb.com"]
    start_urls = ('https://healthyceleb.com/category/statistics/sports-stars/female-sports-stars/page/5',)
    custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["id", "Name", "Gender", "Height", "Weight", "url"],
  }

    '''def parse(self, response):      # this fucntion crawls to different pages
        for i in range(2,20):
            temp = self.start_urls[0]
            nlink = temp.split()[0]
            newlink = nlink[:-1] + str(i),
            self.start_urls = self.start_urls + newlink
            yield scrapy.Request(newlink[0], callback = self.Nparse)'''
    
    def parse (self, response):     # this function choose from 20 different profiles in a page to scrape data
        links = response.xpath('//*[@class="td-ss-main-content"]//h3/a/@href').extract()
        print(links)
        for link in links:
            abs_url = response.urljoin(link)
            yield scrapy.Request(abs_url, callback = self.parse_indetail)

    def parse_indetail(self, response):
        item = FemalesItem()
        item['id'] = response.url.split("/")[-1]
        #print(item['id'])
        
        #item['Name'] = response.xpath('//*/strong[contains(text(),"Quick Info")]/text()').extract_first().replace("Quick Info", "")
        item['Name'] = response.xpath('//*[@id="post-'+str(response.url.split("/")[-1])+'"]/div[1]/header/h1/text()').extract_first()

        item['Gender'] = response.xpath('//*[@id="td-outer-wrap"]/div[2]/div/div[1]/div/span[3]/a/text()').extract_first().split()[0]
        
        item['Height'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"cm")]/text()').extract_first().split("or")[1].replace("cm", "")
        
        item['Weight'] = response.xpath('//*[@class="td-post-content"]/p[contains(text(),"kg")]/text()').extract_first().split("or")[0].replace("kg", "")
        ##item['Weight'] = response.xpath('//*[@id="post-'+str(response.url.split("/")[-1])+'"]/div[3]/table/tbody/tr[2]/td[2]/text()').extract_first().replace("kg", "")
        #item['Weight'] = response.xpath('//*[@id="post-'+str(response.url.split("/")[-1])+'"]/div[3]/p[14]/text()').extract_first().split("or")[0].replace("kg", "")
        item['url'] = response.url
        yield item