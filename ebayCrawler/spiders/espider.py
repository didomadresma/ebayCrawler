#This spider pull next info from ebay product search list:
# Name, link, cost, country, img. url
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor as lle
from scrapy.selector import Selector

class espider(CrawlSpider):
    name = "espider"
    download_delay = 4
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=coffee+maker&_ipg=25&rt=nc']

    rules = (
    	Rule(lle(allow=r'http://www\.ebay\.com/sch/i\.html\?_from=R40&_sacat=0&_nkw=coffee\+maker&_ipg=25&rt=nc'), 
    		callback='parse_item', follow=True),
    	)

    def parse_item(self, response):
    	nameList = response.xpath('//*[@id="ListViewInner"]/li/h3/a/text()').extract()
        linkList = response.xpath('//*[@id="ListViewInner"]/li/h3/a/@href').extract()
        
        raw_costList = response.xpath('//*[@id="ListViewInner"]/li/ul[@class="lvprices left space-zero"]').extract()
        costList = []
        for htmlpart in raw_costList:#extract first cost
            raw_cost = Selector(text=htmlpart).xpath('//ul[@class="lvprices left space-zero"]/li[@class="lvprice prc"]/span/text()').extract_first()
            try:
                result = raw_cost[raw_cost.index('$')+1:]
            except:
                result = '-'
            costList.append(result)
        
        countryList_raw = response.xpath('//*[@id="ListViewInner"]/li/ul[@class="lvdetails left space-zero full-width"]/li/text()').extract()
        countryList = []
        for cnt in countryList_raw:# clear country list
            if cnt.isspace() == False:
                cnt = cnt[cnt.index('F'):]
                countryList.append(cnt)
            else:
                pass

        imgUrlList = response.xpath('//*[@id="ListViewInner"]/li/div/div/a/img/@src').extract()

        for i in range(len(nameList)):
            yield {
            "name" : nameList[i],
            "link" : linkList[i],
            "cost" : costList[i],
            "country" : countryList[i],
            "imgUrl" : imgUrlList[i]
            }