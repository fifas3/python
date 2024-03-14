# boss爬虫数据
import time
from datetime import datetime
import os
import requests
import json
import pandas as pd
from openpyxl.workbook import Workbook

class boss_cv():
    lastPath = os.path.abspath('..')
    couse_list = []
    confHeaders = {}
    _url = 'https://www.zhipin.com/wapi/zpgeek/pc/recommend/job/list.json?city=101070200&experience=&payType=&partTime=&degree=&industry=&scale=&salary=&jobType=&encryptExpectId=cb1494e0c1011eccynU~&mixExpectType=7&page=1&pageSize=15'
    def getConfig(self):
        # 读取配置文件，按照bossconfig进行更新
        fCookie = open(self.lastPath + '/prequest/bossconfig.txt', 'r', encoding='gbk', errors='ignore')
        data = fCookie.readlines()
        for d in data:
            key, value = d.strip().split(':')
            self.confHeaders[key.replace("'", "").strip()] = value.replace("'", "").strip()
        fCookie.close()

    def login_user(self, url):
        print(login_user)

    def fetch_data(self, url):
        self.getConfig()
        time.sleep(2)
        res = requests.get(url, headers=self.confHeaders)
        if res.status_code == 200:
            # 获取从接口的数据
            data=res.json()
            print(f'{data}')
        else:
            print('error')

    def __init__(self):
        self.fetch_data(self._url)
        df = pd.DataFrame(self.couse_list, columns=['title', 'title'])
        current_timestamp = datetime.now().timestamp()
        lastdata='lastData' + str(current_timestamp)
        df.to_excel(f'{lastdata}.xls', index=False, engine="openpyxl")


if __name__=='__main__':
    boss_cv()
    print('OK')
