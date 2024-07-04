import numbers
class animal():
    def is_integer(self,value):
        return isinstance(value, int)
    def zodiac_signs(self, year):
        zodiac_signs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
        return zodiac_signs[(int(year) - 4) % 12]

    def contains_chinese(self,s):
        if isinstance(s, (list, tuple, str)):
            for char in s:  
                if '\u4e00' <= char <= '\u9fff':  # 基本汉字范围  
                    return True  
            return False
        
    def is_float(self,value):  
        return isinstance(value, float)

    def get_liuhai(self,zodiac):
        liuhai_pairs = {
            '鼠与羊': '六害',
            '牛与马': '六害',
            '虎与蛇': '六害',
            '兔与龙': '六害',
            '猴与猪': '六害',
            '鸡与狗': '六害',
            '羊与鼠': '六害',
            '马与牛': '六害',
            '蛇与虎': '六害',
            '龙与兔': '六害',
            '猪与猴': '六害',
            '狗与鸡': '六害'
        }
        if zodiac[0] == zodiac[-1]:
            return '' #无六害
        return liuhai_pairs.get(zodiac, '') #无六害


    def get_liuchong(self,zodiac):
        liuchong_pairs = {
            '鼠与马': '六冲',
            '牛与羊': '六冲',
            '虎与猴': '六冲',
            '兔与鸡': '六冲',
            '龙与狗': '六冲',
            '蛇与猪': '六冲',
            '马与鼠': '六冲',
            '羊与牛': '六冲',
            '猴与虎': '六冲',
            '鸡与兔': '六冲',
            '狗与龙': '六冲',
            '猪与蛇': '六冲'
        }
        if zodiac[0] == zodiac[-1]:
            return '' # 无六冲
        return liuchong_pairs.get(zodiac, '') # 无六冲

    def get_liuhe(self,zodiac):
        liuhe_pairs = {
            '鼠与牛': '六合',
            '猪与虎': '六合',
            '狗与兔': '六合',
            '鸡与龙': '六合',
            '猴与蛇': '六合',
            '马与羊': '六合',
            '牛与鼠': '六合',
            '虎与猪': '六合',
            '兔与狗': '六合',
            '龙与鸡': '六合',
            '蛇与猴': '六合',
            '羊与马': '六合'
        }
        if zodiac[0] == zodiac[-1]:
            return '' # 无合
        return liuhe_pairs.get(zodiac, '') # 无合

    def calculate_benmingnian(self,start_year, end_year, birth_year):
        birth_years = []
        current_year = start_year
        while current_year <= end_year:
            if (current_year - birth_year) % 12 == 0:
                birth_years.append(current_year)
            current_year += 1
        return birth_years

    # 定义拼接属相的函数
    def combine_zodiac(self,row):
        return row['属相_x'] + ' - ' + row['属相_y']