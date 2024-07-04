# coding=utf-8

import pymysql

class DBUtil:

	def __init__(self, host, port, database, user, password):
		try:
			# 连接
			print('连接数据库')
			self.__conn = pymysql.connect(host=host, port=port, database=database, user=user, password=password, charset="utf8")
			# 获取光标
			self.__cursor = self.__conn.cursor()
		except Exception as e:
			print('数据库连接失败！')
			print(e)

	def select(self, sql, args=()):
		items = []
		try:
			self.__cursor.execute(sql, args)
			result = self.__cursor.fetchall()
			for re in result:
				if re is None:
					break
				items.append(re)
		except Exception as e:
			print(e)
			self.__conn.rollback()  # 捕捉到错误就回滚
		# print(items)
		return items

	# 返回自增主键ID
	def insert(self, sql, args=()):
		try:
			self.__cursor.execute(sql, args)
			i = int(self.__cursor.lastrowid)
			self.__conn.commit()
			return i
		except Exception as e:
			print(e)
			self.__conn.rollback()

	def update(self, sql, args=()):
		try:
			i = self.__cursor.execute(sql, args)
			self.__conn.commit()
			return i
		except Exception as e:
			print(e)
			self.__conn.rollback()

	def delete(self, sql, args=()):
		try:
			i = self.__cursor.execute(sql, args)
			self.__conn.commit()
			return i
		except Exception as e:
			print(e)
			self.__conn.rollback()

	def closeDB(self):
		self.__cursor.close()
		self.__conn.close()


# 连接数据库
db = DBUtil('localhost', 3306, 'newsina', 'root', '')


# 导入城市表
# file = open('/Users/maozi/Desktop/city.json', 'r')
# content = file.read()
# select_sql = 'select * from city where province = %s and name = %s'
# insert_sql = 'insert into city(province,name) values (%s,%s)'
# if content:
# 	json_obj = demjson.decode(content)
# 	for provinces in json_obj['provinces']:
# 		province = provinces['provinceName']
# 		for city in provinces['citys']:
# 			name = city['citysName']
# 			select_result = db.select(select_sql, (province, name))
# 			if len(select_result) == 0:
# 				insert_id = db.insert(insert_sql, (province, name))
# 				print '数据插入成功 id = ' + str(insert_id) if (insert_id > 0) else '数据插入失败'
# file.close()

# 更新城市ID
# select_company_sql = 'select id,register_address from company'
# company_result = db.select(select_company_sql)
# # company_result = [company_result[0]]
# for company in company_result:
# 	company_id = company[0]
# 	register_address = company[1]
# 	if register_address is not None:
# 		match_result = re.search(u'(?P<province>[^省]+自治区|.*?省|.*?市)(?P<city>[^市]+自治州|.+盟|市辖区|.*?市)', register_address)
# 		if match_result is not None:
# 			province = match_result.group('province')
# 			city = match_result.group('city')
# 			select_city_sql = 'select * from city where province=%s and name=%s'
# 			print 'company_id = ' + str(company_id) + ', province = ' + province + ', city = ' + city
# 			select_city_result = db.select(select_city_sql, (province, city))
# 			if len(select_city_result) == 1:
# 				city_id = select_city_result[0][0]
# 				update_company_sql = 'update company set city_id = %s where id = %s'
# 				update = db.update(update_company_sql, (city_id, company_id))
# 				print '数据更新成功' if (update > 0) else '数据更新失败'


# 判断行业是否存在
def query_industry(name):
	select_industry_sql = 'select * from industry where name = %s'
	result = db.select(select_industry_sql, (name,))
	if len(result) == 0:
		return 0
	elif len(result) == 1:
		return result[0][0]
	else:
		return None


# 导入证监会公司简单信息及行业分类,数据来源：证监会2019年第二季度报表
# industry_file = openpyxl.load_workbook('/Users/maozi/Desktop/sy-edu/2019年第二季度A股上市公司列表.xlsx')
# new_workbook = openpyxl.Workbook()
# new_sheet = new_workbook.active
# new_rows = []
# for industry_sheet in industry_file.worksheets:
# 	for index, industry_row in enumerate(industry_sheet.rows):
# 		first_type = industry_row[0].value
# 		sub_type = industry_row[2].value
# 		code = industry_row[3].value
# 		stock_name = industry_row[4].value
# 		# new_rows.append(code)
# 		# if first_type is not None:
# 		# 	first_type = first_type.strip()
# 		# 	if first_type != '' and first_type != u'门类名称及代码' and first_type != u'(A)' and query_industry(first_type) == 0:
# 		# 		insert_sql = 'insert into industry(name) values (%s)'
# 		# 		insert_id = db.insert(insert_sql, (first_type,))
# 		# 		print ('数据插入成功' + str(insert_id)) if (insert_id > 0) else '数据插入失败'
# 		# if sub_type is not None:
# 		# 	sub_type = sub_type.strip()
# 		# 	if sub_type != '' and sub_type != u'行业大类名称' and query_industry(sub_type) == 0:
# 		# 		insert_sql = 'insert into industry(name) values (%s)'
# 		# 		insert_id = db.insert(insert_sql, (sub_type,))
# 		# 		print ('数据插入成功' + str(insert_id)) if (insert_id > 0) else '数据插入失败'
# 		if stock_name is not None and code is not None:
# 			code = code.strip()
# 			stock_name = stock_name.strip()
# 			# print 'stock_name = ' + stock_name + ', code = ' + code + ', industry = ' + sub_type
# 			select_corp_sql = 'select * from company where code = %s'
# 			corp_result = db.select(select_corp_sql, (code,))
# 			industry_id = query_industry(sub_type)
# 			if len(corp_result) == 1 and industry_id > 0:
# 				print 'stock_name = ' + stock_name + ', code = ' + code + ', industry = ' + sub_type
# 				update_corp_sql = 'update company set industry = %s where stock_name = %s'
# 				update = db.update(update_corp_sql, (sub_type, stock_name))
# 				print '数据更新成功' if (update > 0) else '数据更新失败'
# 			elif len(corp_result) == 0:
# 				print u'不存在的：stock_name = ' + stock_name + u', code = ' + code + u', industry = ' + sub_type
# 				new_rows.append([industry_row[0].value, industry_row[1].value, industry_row[2].value, industry_row[3].value, industry_row[4].value])
# 		print '======================'
# # print u','.join(new_rows)
# for i in new_rows:
# 	new_sheet.append(i)
# new_workbook.save('数据对比-证监会.xlsx')


# 判断是否是校友
def school_fellow(content, *args):
	flag = False
	for arg in args:
		if content.find(arg) != -1:
			flag = True
	return flag


# 判断学历
def get_education(arg):
	if arg.find(u'博士后') != -1:
		name = u'博士后'
	elif arg.find(u'博士') != -1:
		name = u'博士'
	elif arg.find(u'硕士') != -1 or arg.find(u'MBA') != -1 or arg.find(u'研究生') != -1:
		name = u'硕士'
	elif arg.find(u'学士') != -1 or arg.find(u'本科') != -1:
		name = u'学士'
	else:
		return None
	sql = 'select id from education where name = %s '
	result = db.select(sql, (name,))
	if len(result) > 0:
		return result[0][0]


# 获取校友企业逻辑
# v1 - 关键字匹配
# 查询大学列表
# select_school_sql = 'select id,name from school'
# school_result = db.select(select_school_sql)
# # school_result = [school_result[0]]
# for school in school_result:
# 	school_id = school[0]
# 	school_name = school[1]
# 	# 查询不存在校友列表的校友
# 	select_school_person_sql = 'select person_id from person_school where school_id = %s'
# 	school_person_result = db.select(select_school_person_sql, (school_id,))
# 	if len(school_person_result) == 0:
# 		school_person_ids = u'0'
# 	else:
# 		school_person_ids = ','.join(str(i[0]) for i in school_person_result)
# 	# 查询person列表
# 	select_person_sql = 'select id,highest_degree,detail from base_person where id not in (' + school_person_ids + ')'
# 	person_result = db.select(select_person_sql)
# 	# person_result = [person_result[338]]
# 	for person in person_result:
# 		person_id = person[0]
# 		education = person[1]
# 		detail = person[2]
# 		# 排除浙大本科以下学历
# 		education_id = get_education(education)
# 		if school_fellow(detail, school_name) and education_id is not None:
# 			print 'id = ' + str(person_id) + ', education = ' + education + ', detail = ' + detail
# 			# 保存校友与学校关系
# 			insert_school_person_sql = 'insert into person_school (school_id, person_id) values (%s, %s)'
# 			school_person_insert = db.insert(insert_school_person_sql, (school_id, person_id))
# 			print '数据插入成功 id=' + str(school_person_insert) if (school_person_insert > 0) else '数据插入失败'
# 			# 保存校友学历信息
# 			select_education_sql = 'select * from person_education where person_id = %s and education_id = %s and school_id = %s '
# 			education_result = db.select(select_education_sql, (person_id, education_id, school_id))
# 			if len(education_result) == 0:
# 				insert_education_person_sql = 'insert into person_education (person_id, education_id, school_id) values (%s, %s, %s)'
# 				person_education_insert = db.insert(insert_education_person_sql, (person_id, education_id, school_id))
# 				print '数据插入成功 id=' + str(person_education_insert) if (person_education_insert > 0) else '数据插入失败'
# 			# 查询校友属于公司列表
# 			select_base_person_company_sql = 'select company_id,position,start_time,end_time from base_person_company where person_id = %s'
# 			base_person_company_result = db.select(select_base_person_company_sql, (person_id,))
# 			for base_person_company in base_person_company_result:
# 				company_id = base_person_company[0]
# 				position = base_person_company[1]
# 				start_time = base_person_company[2]
# 				end_time = base_person_company[3]
# 				# insert_person_company_sql = 'insert into person_company (company_id,person_id,school_id,position,start_time,end_time) values (%s,%s,%s,%s,%s,%s)'
# 				# person_company_insert = db.insert(insert_person_company_sql, (company_id, person_id, school_id, position, start_time, end_time))
# 				# print '数据插入成功 id=' + str(person_company_insert) if (person_company_insert > 0) else '数据插入失败'
# 				select_school_company_sql = 'select * from school_company where company_id = %s and school_id = %s'
# 				school_company_result = db.select(select_school_company_sql, (company_id, school_id))
# 				if len(school_company_result) == 0:
# 					# 查询公司信息
# 					select_company_sql = 'select stock_name,industry from company where id = %s'
# 					print company_id
# 					company_result = db.select(select_company_sql, (company_id,))
# 					if len(company_result) == 1:
# 						# 公司默认简称是股票简称
# 						company_name = company_result[0][0]
# 						industry_name = company_result[0][1]
# 						print industry_name
# 						select_industry_sql = 'select id from industry where name = %s'
# 						industry_result = db.select(select_industry_sql, (industry_name,))
# 						industry_id = None
# 						if len(industry_result) == 1:
# 							industry_id = industry_result[0][0]
# 						# 保存企业与学校关系
# 						insert_school_company_sql = 'insert into school_company (company_id, school_id,company_name,industry_id) values (%s, %s, %s, %s)'
# 						school_company_insert = db.insert(insert_school_company_sql, (company_id, school_id, company_name, industry_id))
# 						print '数据插入成功 id=' + str(school_company_insert) if (school_company_insert > 0) else '数据插入失败'


# # 中国经济区划分
# select_company_sql = 'select id,city_id from company'
# company_result = db.select(select_company_sql)
# for company in company_result:
# 	company_id = company[0]
# 	city_id = company[1]
# 	select_city_sql = 'select province,name from city where id = %s'
# 	city_result = db.select(select_city_sql, (city_id,))
# 	if len(city_result) == 1:
# 		province = city_result[0]
# 		city_name = city_result[1]
# 		select_region_sql = 'select id from region where locate(%s,detail)'
# 		region_result = db.select(select_region_sql, (province,))
# 		if len(region_result) == 1:
# 			region_id = region_result[0][0]
# 			print 'company_id = ' + str(company_id) + '  region_id = ' + str(region_id)
# 			update_company_sql = 'update company set region_id = %s where id = %s'
# 			update = db.update(update_company_sql, (region_id, company_id))
# 			print '数据更新成功' if (update > 0) else '数据更新失败'
# 		select_region_sql = 'select id from region where locate(%s,detail)'
# 		region_result = db.select(select_region_sql, (city_name,))
# 		if len(region_result) == 1:
# 			region_id = region_result[0][0]
# 			print 'company_id = ' + str(company_id) + '  region_id = ' + str(region_id)
# 			update_company_sql = 'update company set region_id = %s where id = %s'
# 			update = db.update(update_company_sql, (region_id, company_id))
# 			print '数据更新成功' if (update > 0) else '数据更新失败'
