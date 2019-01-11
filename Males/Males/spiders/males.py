import scrapy


class Male(scrapy.Spider):
    name = "male"
    allowed_domains = ["healthyceleb.com"]
    start_urls = ('https://healthyceleb.com/category/statistics/sports-stars/male-sports-stars/page/1',)

    def parse (self, response):
        links = response.xpath('//div[@class="td_module_1 td_module_wrap td-animation-stack td-meta-info-hide"]/h3[@class="entry-title td-module-title"]/a/@href').exctract()
        i = 1
        e = 1
        o = 2
        for link in links:
            abs_url = response.urljoin(link)
            if i%2 == 0:
                url_next = '//*[@id="td-outer-wrap"]/div[4]/div/div/div[1]/div/div['+str(i+1)+']/div['+str(e)+']/div/h3/a/text()'
            else:
                url_next = '//*[@id="td-outer-wrap"]/div[4]/div/div/div[1]/div/div['+str(i+1)+']/div['+str(o)+']/div/h3/a/text()'
            rating = response.xpath(url_next).exctract()
            if (i <= len(links)):
                i=i+1
            yield scrapy.Request(abs_url, callback = self.parse_indetail, meta={'rating' : rating})

    def parse_indetail(self, response):
        item = MalesItem()
        item['id'] = response.xpath('/html/head/link[4]/text()').exctract[0][:-1]
        
        item['Name'] = response.xpath('//*[@id="post-120352"]/div[3]/p[1]/strong/text()').exctract()[0]
        
        item['Gender'] = response.xpath('//*[@id="td-outer-wrap"]/div[2]/div/div[1]/div/span[3]/a/text()').exctract()
        
        item['Height'] = response.xpath('//*[@id="post-120352"]/div[3]/p[16]/text()').exctract()[-1]
        
        item['Weight'] = response.xpath('//*[@id="post-120352"]/div[3]/table/tbody/tr[2]/td[2]/text()').exctract()

        item['url'] = response.xpath('/html/head/link[4]/text()').exctract()

        return item