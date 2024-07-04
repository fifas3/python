# -*- coding: utf-8 -*-
import demjson3 as demjson
from stock_cn.items import *
from bs4 import BeautifulSoup
import requests
import re
import time


# 股票爬虫
class StockSpider(scrapy.Spider):
	name = 'StockSpider'
	allowed_domains = ['vip.stock.finance.sina.com.cn']
	start_urls = ['http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=sort']
	page = 1
	custom_settings = {
		'ITEM_PIPELINES': {
			'stock_cn.pipelines.StockCnPipeline': 300
		}
	}

	def parse(self, response):
		print('page = ' + str(self.page))
		result = response.text
		if result != 'null' and result is not None:
			result = demjson.decode(result)
			# result = [result[1]]
			for index, i in enumerate(result):
				# if (self.page == 7 and index > 8) or self.page > 7:
				if self.page >= 1:
					stock_item = StockItem()
					stock_item['symbol'] = i['symbol']
					stock_item['code'] = i['code']
					stock_item['stock_name'] = i['name']
					stock_item['share_price'] = i['trade']
					capital = self.stock_parse(i['symbol'])
					if capital:
						stock_item['capital'] = capital
						stock_item['market_cap'] = float(i['trade']) * capital
					else:
						stock_item['capital'] = None
						stock_item['market_cap'] = None
					growth_rate = self.financial_parse(i['code'])
					if growth_rate:
						stock_item['growth_rate'] = growth_rate
					else:
						stock_item['growth_rate'] = None
					yield stock_item
			self.page += 1
			next_page_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=' + str(self.page) + '&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page'
			yield scrapy.Request(next_page_url, callback=self.parse)

	# 获取总股本/万股
	def stock_parse(self, symbol):
		time.sleep(1.4)
		url = 'https://finance.sina.com.cn/realstock/company/' + symbol + '/nc.shtml'
		html = requests.get(url)
		soup = BeautifulSoup(html.content, features='html.parser')
		p_selector = soup.find('div', {'class': 'com_overview blue_d'}).find_all('p')
		if len(p_selector) > 13:
			return float(re.search(r'\d+\.?\d+', p_selector[12].get_text()).group(0))

	# 获取增长率
	def financial_parse(self, code):
		time.sleep(1.6)
		url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/' + code + '/displaytype/4.phtml'
		html = requests.get(url)
		soup = BeautifulSoup(html.content, features='html.parser')
		table = soup.find('table', id='BalanceSheetNewTable0')
		pcp = table.find('td', text='总资产增长率(%)')
		if pcp is not None:
			if pcp.next_sibling.text != '--':
				return float(pcp.next_sibling.text)
			if pcp.next_sibling.next_sibling.text != '--':
				return float(pcp.next_sibling.next_sibling.text)
			if pcp.next_sibling.next_sibling.next_sibling.text != '--':
				return float(pcp.next_sibling.next_sibling.next_sibling.text)
			if pcp.next_sibling.next_sibling.next_sibling.next_sibling.text != '--':
				return float(pcp.next_sibling.next_sibling.next_sibling.next_sibling.text)
