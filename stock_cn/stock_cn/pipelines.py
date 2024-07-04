# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from stock_cn.DBUtil import db
from stock_cn.items import *
import re
from stock_cn.common import animal


class StockCnPipeline:

	def process_item(self, item, spider):
		# 股票持久化
		self.def_animal = animal()
		if isinstance(item, StockItem):
			print('====================== StockItem  ========================')
			select_sql = 'select * from company where code=%s'
			select_result = db.select(select_sql, (item['code'],))
			if len(select_result) == 0:
				insert_sql = "insert into company(symbol,code,stock_name,share_price,capital,market_cap,growth_rate) values (%s,%s,%s,%s,%s,%s,%s)"
				db.insert(insert_sql, (item['symbol'], item['code'], item['stock_name'].replace(u' ', ''), item['share_price'], item['capital'], item['market_cap'], item['growth_rate']))
				print('数据插入成功')
			else:
				 update_sql = 'update company set share_price=%s, capital=%s, market_cap=%s, growth_rate=%s where code=%s'
				# update = db.update(update_sql, (item['share_price'], item['capital'], item['market_cap'], item['growth_rate'], item['code']))
				# print('数据更新成功' if (update > 0) else '数据更新失败1')
		# 公司持久化
		elif isinstance(item, CorpInfoItem):
			print('====================== CorpInfoItem  ========================')
			select_company_sql = 'select id from company where code=%s'
			company_result = db.select(select_company_sql, (item['code'],))
			if len(company_result) == 1:
				corp_id = company_result[0][0]
				# 处理城市
				city_id = None
				register_address = item['register_address'].encode('utf-8')
				print(register_address)
				if register_address.find('省') != -1:
					province = register_address[0:register_address.find('省')]
					if register_address.find('市') != -1:
						city = register_address[(register_address.find('省') + 3):register_address.find('市')]
						select_city_sql = 'select * from city where province=%s and name=%s'
						print('province = ' + province + ' , city = ' + city)
						select_city_result = db.select(select_city_sql, (province, city))
						if len(select_city_result) == 1:
							city_id = select_city_result[0][0]
				else:
					if register_address.find('市') != -1:
						province = city = register_address[0:register_address.find('市')]
						select_city_sql = 'select * from city where province=%s and name=%s'
						print('province = ' + province + ' , city = ' + city)
						select_city_result = db.select(select_city_sql, (province, city))
						if len(select_city_result) == 1:
							city_id = select_city_result[0][0]
				update_sql = 'update company set name=%s, eng_name=%s,city_id=%s, register_address=%s, industry=%s, create_time=%s, registered_capital=%s, org_form=%s, tel=%s, homepage=%s, register_address=%s, introduce=%s, business_scope=%s where id=%s'
				update = db.update(update_sql, (item['name'], item['eng_name'], city_id, item['register_address'], item['industry'], item['create_time'], item['registered_capital'], item['org_form'], item['tel'], item['homepage'], item['register_address'], item['detail'], item['business_scope'], corp_id))
				print('数据更新成功' if (update > 0) else '数据更新失败2')
		# 高管持久化
		elif isinstance(item, CorpManagerInfoItem):
			print('====================== CorpManagerInfoItem  ========================')
			select_company_sql = 'select * from company where code = %s'
			company_result = db.select(select_company_sql, (item['code'],))
			if item['sex'] == '男':
				sex = 1
			elif item['sex'] == '女':
				sex = 2
			else:
				sex = 0
			birth = None
			if item['birth'] is not None:
				birth = re.search(r'^\d{4}', item['birth']).group(0)
				animal_value = self.def_animal.zodiac_signs(birth)
			select_person_sql = 'select * from person where name=%s and sex=%s and birth=%s and position=%s and start_date=%s and end_date=%s'
			person_result = db.select(select_person_sql, (item['name'], sex, birth, item['position_name'], item['start_date'], item['end_date']))
			if len(company_result) == 1 and len(person_result) == 0:
				insert_sql = 'insert into person(code,name,sex,birth,highest_degree,detail,start_date, end_date,position,animal) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				db.insert(insert_sql, (item['code'], item['name'], sex, birth, item['education'], item['detail'], item['start_date'], item['end_date'], item['position_name'], animal_value))
				if item['position_name'] == '董事长':
					insert_sql = 'insert into person_dsz(code,name,sex,birth,highest_degree,detail,start_date, end_date,position,animal,position_code) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
					db.insert(insert_sql, (item['code'], item['name'], sex, birth, item['education'], item['detail'], item['start_date'], item['end_date'],item['position_name'], animal_value,'10'))

		elif isinstance(item, NewsItem):
			print('====================== NewsItem  ========================')
			select_company_sql = 'select * from company where code = %s'
			company_result = db.select(select_company_sql, (item['symbol'],))
			corp_id = company_result[0][0]
			if corp_id:
				select_news_sql = 'select * from news where company_id = %s and title = %s and url = %s'
				news_result = db.select(select_news_sql, (corp_id, item['title'], item['url']))
				if len(news_result) == 0:
					insert_news_sql = 'insert into news (company_id,title,url,create_time) values (%s, %s, %s, %s)'
					insert_id = db.insert(insert_news_sql, (corp_id, item['title'], item['url'], item['create_time']))
					print ('数据插入成功' + str(insert_id))
				elif len(news_result) == 1:
					id = news_result[0][0]
					update_new_sql = 'update news set create_time = %s where id = %s'
					update = db.update(update_new_sql, (item['create_time'], id))
					print('数据更新成功' if (update > 0) else '数据更新失败3' + str(update))
		return item
