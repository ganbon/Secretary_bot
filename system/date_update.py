from datetime import datetime


class Date_Update:
    def __init__(self):
        now_date = datetime.now()
        self.week_list = ["月曜", "火曜", "水曜", "木曜", "金曜", "土曜", "日曜"]
        self.week = datetime.today().weekday()
        self.year = int(now_date.year)
        self.month = int(now_date.month)
        self.day = int(now_date.day)
        self.key_week = self.week
        self.special_month = [2, 4, 6, 9, 11]
        

    # 曖昧な表現を正確な日程に変換                                      
    def convert(self, sentences):
        if "来年" in sentences:
            year = self.year+1
            sentences = sentences.replace("来年",str(year))
        if "今日" in sentences:
            year = self.year
            month = self.month
            day = self.day
            sentences = sentences.replace("今日",f"{year}年{month}月{day}日")
        if "明日" in sentences:
            year, month, day = self.day_set(1)
            sentences = sentences.replace("明日",f"{year}年{month}月{day}日")
        if  "明後日" in sentences:
            year,month,day = self.day_set(2)
            sentences = sentences.replace("明後日",f"{year}年{month}月{day}日")
        if "明々後日" in sentences:
            year,month,day=self.day_set(3)
            sentences=sentences.replace("明々後日",f"{year}年{month}月{day}日")
        if "再来月" in sentences:
            year,month = self.month_set(2)
            sentences=sentences.replace("再来月",f"{year}年{month}月")
        if "来月" in sentences:
            year,month = self.month_set(1)
            sentences = sentences.replace("来月",f"{year}年{month}月")
        elif "今月" in sentences:
            year,month = self.year,self.month
            sentences = sentences.replace("今月",f"{year}年{month}月")
        for w in self.week_list:
            if w in sentences:
                self.key_week = self.week_list.index(w)
        if "再来週" in sentences:
            diff = 14-(self.week-self.key_week)
            year,month,day = self.day_set(diff)
            sentences = sentences.replace("再来週","")
        elif "来週" in sentences:
            diff = 7-(self.week-self.key_week)
            year,month,day = self.day_set(diff)
            sentences = sentences.replace("来週","")
        elif "今週" in sentences:
            diff = self.key_week-self.week
            year,month,day = self.day_set(diff)
            sentences = sentences.replace("今週","")
        if self.week_list[self.key_week]+"日" in sentences:
            sentences = sentences.replace(self.week_list[self.key_week]+"日",f"{year}年{month}月{self.day}日")
        elif self.week_list[self.key_week] in sentences:
            sentences = sentences.replace(self.week_list[self.key_week],f"{year}年{month}月{self.day}日")   
        return sentences
                
    # 日にちの変換
    def day_set(self, diff_num):
        year = self.year
        month = self.month
        day = self.day
        if month == 12 and day+diff_num > 31:
            year = year+1
            month = 1
            day += diff_num-31
        elif month == 2 and day+diff_num > 27:
            if year % 4 == 0:
                if year % 100 == 0 and self.day == 28:
                    month = self.month+1
                    day += diff_num-28
                elif year % 400 == 0 and day == 29:
                    month = self.month+1
                    day += diff_num-29
        elif month not in self.special_month and day + diff_num > 31:
            month = month+1
            day += diff_num-31
        elif month in self.special_month and day + diff_num > 30:
            month = month+1
            day += diff_num-30
        else:
            day += diff_num
        self.year = year
        self.month = month
        self.day = day
        self.week += diff_num%7
        return year, month, day

    # 月の変換
    def month_set(self, diff_num):
        year = self.year
        month = self.month
        if month+diff_num > 13:
            year += 1
            month = 1
        else:
            month += diff_num
        self.year = year
        self.month = month
        return year, month

'''
d=Date_Update()
e=input()
s=d.convert(e)
print(s)
'''