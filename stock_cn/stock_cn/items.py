# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockCnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 股票item
class StockItem(scrapy.Item):
	symbol = scrapy.Field()
	code = scrapy.Field()
	stock_name = scrapy.Field()
	share_price = scrapy.Field()
	capital = scrapy.Field()
	market_cap = scrapy.Field()
	growth_rate = scrapy.Field()


# 公司详情item
class CorpInfoItem(scrapy.Item):
	code = scrapy.Field()
	name = scrapy.Field()
	eng_name = scrapy.Field()
	create_time = scrapy.Field()
	registered_capital = scrapy.Field()
	org_form = scrapy.Field()
	tel = scrapy.Field()
	homepage = scrapy.Field()
	register_address = scrapy.Field()
	industry = scrapy.Field()
	detail = scrapy.Field()
	business_scope = scrapy.Field()


# 高管item
class CorpManagerInfoItem(scrapy.Item):
	code = scrapy.Field()
	name = scrapy.Field()
	sex = scrapy.Field()
	birth = scrapy.Field()
	education = scrapy.Field()
	detail = scrapy.Field()
	position = scrapy.Field()
	position_name = scrapy.Field()
	start_date = scrapy.Field()
	end_date = scrapy.Field()


# 高管职位item
class ManagerPositionItem(scrapy.Item):
	title = scrapy.Field()
	start_time = scrapy.Field()
	end_time = scrapy.Field()


# 新闻item
class NewsItem(scrapy.Item):
	symbol = scrapy.Field()
	title = scrapy.Field()
	url = scrapy.Field()
	create_time = scrapy.Field()
