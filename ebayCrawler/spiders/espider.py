#This spider pull next info from ebay product search list:
# Name, link, cost, country, img. url
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request

class espider(scrapy.Spider):
    name = "espider"
    #download_delay = 4
    allowed_domains = ['ebay.com']
    start_urls = ['http://www.ebay.com/sch/i.html?_from=R40&_sacat=0&_nkw=coffee+maker&_pgn=1&_skc=25&rt=nc']

    def parse(self, response):
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

        # Not all imgUrls pull correct  if use >
        #imgUrlList = response.xpath('//*[@id="ListViewInner"]/li/div/div/a/img/@src').extract()
        imgUrlList = []
        for link in linkList:
        	#imgUrl example "http://thumbs.ebaystatic.com/images/g/B80AAOSwZQRYaBjw/s-l225.jpg"
        	#part B80AAOSwZQRYaBjw extract from item link
        	index = link.rindex(':')
        	imgUrl = "http://thumbs.ebaystatic.com/images/g/" + link[index+1:] + "/s-l225.jpg"
        	imgUrlList.append(imgUrl)

        for i in range(len(nameList)):
            try:
            	yield {
            	"name" : nameList[i],
                "link" : linkList[i],
                "cost" : costList[i],
                "country" : countryList[i],
                "imgUrl" : imgUrlList[i]
                }
            except:
            	pass

        crawledLinks = self.start_urls

        nextPageUrl = response.xpath('//*[@class="gspr next"]/@href').extract()[0]
        print("NPU >>> ", nextPageUrl)
        if nextPageUrl != None and len(crawledLinks) < 5:
            crawledLinks.append(nextPageUrl)
            yield Request(response.urljoin(nextPageUrl), callback=self.parse)
        else:
            "nextPageUrl not defined"

        print(crawledLinks)