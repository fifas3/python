# -*- coding: utf-8 -*-
import scrapy
from stock_cn.items import *
from stock_cn.DBUtil import db


# 公司新闻爬虫
class NewsSpider(scrapy.Spider):
	name = 'NewsSpider'
	allowed_domains = ['vip.stock.finance.sina.com.cn']
	custom_settings = {
		'ITEM_PIPELINES': {
			'stock_cn.pipelines.StockCnPipeline': 300
		}
	}

	def start_requests(self):
		select_sql = 'select * from company'
		select_result = db.select(select_sql, ())
		# select_result = [select_result[0]]
		for item in select_result:
			# print(item[0][2:])
			try:
				if int(item[0][2:]) > 0:
					print(item)
					symbol = item[1]
					print('id = ' + str(item[0]) + ', symbol = ' + symbol)
					# 'https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/300456.phtml'
					url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllBulletin/stockid/' + symbol + '.phtml'
					yield scrapy.Request(url, callback=self.parse, meta={'symbol': symbol})
				else:
					print('else ' + item[1])
			except Exception as e:
				print((f"Error processing: {e}"))

	def parse(self, response):
		text_selector = response.css('.datelist ul::text')
		a_selector = response.css('.datelist ul a')
		for index, i in enumerate(a_selector):
			news_item = NewsItem()
			news_item['symbol'] = response.meta['symbol']
			news_item['title'] = i.xpath('string(.)').get()
			news_item['url'] = i.xpath('./@href').get()
			create_time = text_selector[index * 2].get().strip().replace(u'\xa0', ' ') + ':00'
			news_item['create_time'] = create_time
			yield news_item
