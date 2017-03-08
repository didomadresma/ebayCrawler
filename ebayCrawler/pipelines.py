# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2

class EbaycrawlerPipeline(object):
    #def process_item(self, item, spider):
    def __init__(self):
        #user = input("Enter DB username: ")
        #dbname = input("Enter DB name: ")
        try:
        	self.conn = psycopg2.connect("user='postgres' dbname='ebay' password='xenon101292,,'")
        except:
        	print("Error during db connect")

    def process_item(self, item, spider):
        cur = self.conn.cursor()
        try:
        	cur.execute("INSERT INTO ebaytable(name, link, cost, country, imgurl) VALUES(%s,%s,%s,%s,%s)",
        	    (item['name'], item['link'], item['cost'], item['country'], item['imgUrl']))
        except:
        	print("execute error")
        
        try:
        	self.conn.commit()
        except:
        	print("commit error")
        	
        return item