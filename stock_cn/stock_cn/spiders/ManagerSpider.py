# -*- coding: utf-8 -*-
import scrapy
from importlib import reload
from stock_cn.items import *
from stock_cn.DBUtil import db
import sys

reload(sys)
# sys.setdefaultencoding('utf-8')


# 公司高管爬虫
class ManagerSpider(scrapy.Spider):
	name = 'ManagerSpider'
	allowed_domains = [u'vip.stock.finance.sina.com.cn']
	custom_settings = {
		'ITEM_PIPELINES': {
			'stock_cn.pipelines.StockCnPipeline': 300
		}
	}

	def start_requests(self):
		# limit 1

		select_sql = 'select * from company'
		select_result = db.select(select_sql)
		# select_result = [select_result[5]]
		for item in select_result:
			if int(item[0][2:]) >= 1:
				code = item[0][2:]
				url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpManager/stockid/' + code + '.phtml'
				yield scrapy.Request(str(url), self.parse, meta={'code': code})

	def parse(self, response):
		code = response.meta['code']
		count = 0
		for i in response.css('#comInfo1'):
			rows = i.xpath('//table[@id="comInfo1"]/tbody/tr')
			# name = row.xpath('td[1]//text()').get()
			# for row in rows:
			# 	position_name = row.xpath('td[2]//text()').get()
			# 	start_date = row.xpath('td[3]//text()').get()
			# 	end_date = row.xpath('td[4]//text()').get()
			for item_href in i.css('a::attr(href)').getall():
				# corp_manager_info_url = response.urljoin(item_href).encode('gbk')
				corp_manager_info_url = 'https://vip.stock.finance.sina.com.cn/'+item_href
				# print(corp_manager_info_url)
				met = {'code': code}
				yield scrapy.Request(corp_manager_info_url, self.corp_manager_info_parse, meta=met)

	def corp_manager_info_parse(self, response):
		# print(f'开始解析 {response.url}')
		try:
			table1_selector = response.css('#Table1 tbody div')
			# manager_info_item = CorpManagerInfoItem()
			# manager_info_item['code'] = response.meta['code']
			# manager_info_item['name'] = table1_selector[0].css('::text').get()
			# manager_info_item['sex'] = table1_selector[1].css('::text').get()
			# manager_info_item['birth'] = table1_selector[2].css('::text').get()
			# manager_info_item['education'] = table1_selector[3].css('::text').get()
			# manager_info_item['detail'] = response.css('.graybgH::text').get()
			# manager_info_item['start_date'] = response.meta['start_date']
			# manager_info_item['end_date'] = response.meta['end_date']
			# manager_info_item['position_name'] = response.meta['position_name']
			table3_selector = response.css('#Table3')
			div3_selector = table3_selector.css('tbody tr')
			for index, i in enumerate(div3_selector):
				item = i.css('div::text')
				manager_info_item = CorpManagerInfoItem()
				manager_info_item['code'] = response.meta['code']
				manager_info_item['name'] = table1_selector[0].css('::text').get()
				manager_info_item['sex'] = table1_selector[1].css('::text').get()
				manager_info_item['birth'] = table1_selector[2].css('::text').get()
				manager_info_item['education'] = table1_selector[3].css('::text').get()
				manager_info_item['detail'] = response.css('.graybgH::text').get()
				manager_info_item['start_date'] = item[1].get()
				if len(item) == 4:
					manager_info_item['end_date'] = item[2].get()
				else:
					manager_info_item['end_date'] = None
				manager_info_item['position_name'] = item[0].get()
				yield manager_info_item
			# positions = []
			# for index, i in enumerate(div3_selector):
			# 	item = i.css('div::text')
			# 	position_item = ManagerPositionItem()
			# 	position_item['title'] = item[0].get()
			# 	print(item[0].get())
			# 	position_item['start_time'] = item[1].get()
			# 	if len(item) == 3:
			# 		position_item['end_time'] = item[2].get()
			# 	else:
			# 		position_item['end_time'] = None
			# 	positions.append(position_item)
			# manager_info_item['position'] = positions
			# yield manager_info_item
		except Exception as e:
			self.logger.error(f"Error processing {response.url}: {e}")
