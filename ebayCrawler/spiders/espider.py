#This spider pull next info from ebay products list:
# Name, link, cost, country, img. url
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor as lle
from scrapy.selector import Selector

class espider(CrawlSpider):
    name = "espider"
    download_delay = 2
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=coffee+maker&_pgn=1&_skc=100&rt=nc']

    rules = (
    	Rule(lle(allow=r'http://www\.ebay\.com/sch/i\.html\?_from=R40&_sacat=0&_nkw=coffee\+maker&_pgn=[1-10]&_skc=100&rt=nc'), 
    		callback='parse_item', follow=True),
    	)

    def parse_item(self, response):
    	nameList = response.xpath('//*[@id="ListViewInner"]/li/h3/a/text()').extract()
        linkList = response.xpath('//*[@id="ListViewInner"]/li/h3/a/@href').extract()
        costList = response.xpath('//*[@id="ListViewInner"]/li/ul[@class="lvprices left space-zero"]').extract()

        print costList
        #yield {
    	#"name" : response.xpath('//*[@id="ListViewInner"]/li/h3/a/text()').extract()
    	#}
