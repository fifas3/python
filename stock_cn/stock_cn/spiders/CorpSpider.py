# -*- coding: utf-8 -*-
import scrapy
from stock_cn.items import *
import time
from bs4 import BeautifulSoup
import requests
from stock_cn.DBUtil import db


# 公司详情爬虫
class CorpSpider(scrapy.Spider):
	name = 'CorpSpider'
	allowed_domains = ['vip.stock.finance.sina.com.cn']
	custom_settings = {
		'ITEM_PIPELINES': {
			'stock_cn.pipelines.StockCnPipeline': 300
		}
	}

	def start_requests(self):
		select_sql = 'select * from company'
		select_result = db.select(select_sql, ())
		# select_result = [select_result[7]]
		for item in select_result:
			if item[0] > 0:
				code = item[2]
				print('id = ' + str(item[0]) + ', code = ' + code)
				url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/' + code + '.phtml'
				yield scrapy.Request(url, self.parse, meta={'code': code})

	def parse(self, response):
		table_selector = response.css('#comInfo1')
		tr_selector = table_selector.css('tr')
		corp_info_item = CorpInfoItem()
		corp_info_item['code'] = response.meta['code']
		corp_info_item['name'] = tr_selector[0].css('td').xpath('string(.)')[1].get()
		corp_info_item['eng_name'] = tr_selector[1].css('td').xpath('string(.)')[1].get()
		corp_info_item['create_time'] = tr_selector[4].css('td').xpath('string(.)')[1].get()
		corp_info_item['registered_capital'] = tr_selector[4].css('td').xpath('string(.)')[3].get()
		corp_info_item['org_form'] = tr_selector[5].css('td').xpath('string(.)')[3].get()
		corp_info_item['tel'] = tr_selector[6].css('td').xpath('string(.)')[3].get()
		corp_info_item['homepage'] = tr_selector[12].css('td').xpath('string(.)')[3].get()
		corp_info_item['register_address'] = tr_selector[17].css('td').xpath('string(.)')[1].get()
		industry = self.industry_parse(response.meta['code'])
		if industry:
			corp_info_item['industry'] = industry
		else:
			corp_info_item['industry'] = None
		corp_info_item['detail'] = tr_selector[19].css('td').xpath('string(.)')[1].get()
		corp_info_item['business_scope'] = tr_selector[20].css('td').xpath('string(.)')[1].get()
		yield corp_info_item

	def industry_parse(self, code):
		time.sleep(2)
		url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpOtherInfo/stockid/' + code + '/menu_num/2.phtml'
		html = requests.get(url)
		soup = BeautifulSoup(html.content, features='html.parser')
		td_selector = soup.find_all('td', {'class': 'ct'})
		if len(td_selector) > 2:
			return td_selector[1].get_text()
