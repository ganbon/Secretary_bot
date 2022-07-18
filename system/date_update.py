from datetime import datetime,timedelta
from nlptoolsjp.morpheme import morpheme


class Date_Update:
    def __init__(self):
        self.now_date = datetime.now()
        self.week_list = ['月曜', '火曜', '水曜', '木曜', '金曜', '土曜', '日曜']
        self.keyword_year = {"来年":1}
        self.keyword_day = {'今日':0,'明日':1,'明後日':2,'明々後日':3}
        self.keyword_month ={'今月':0,'来月':1,'再来月':2}
        self.keyword_week = {'今週':0,'来週':7,'再来週':14}
        self.week = datetime.today().weekday()
        self.year = int(self.now_date.year)
        self.month = int(self.now_date.month)
        self.day = int(self.now_date.day)
        self.key_week = self.week

    # 曖昧な表現を正確な日程に変換                                      
    def convert(self, message, diff_op = False):
        year = self.year
        month = self.month
        day = self.day
        key_w = None
        diff = -1
        sentences = morpheme(message,nelogd=False)
        for s,sentence in enumerate(sentences):
            if sentence in self.keyword_year.keys():
               year = self.year + self.keyword_year[sentence] 
               diff = self.keyword_day[sentence]
               message = message.replace(sentence, f'{year}年')
            elif sentence in self.keyword_day.keys():
                year, month, day = self.day_set(self.keyword_day[sentence])
                message = message.replace(sentence, f'{year}年{month}月{day}日')
                diff = self.keyword_day[sentence]
            elif sentence in self.keyword_month.keys():
                year, month = self.month_set(self.keyword_month[sentence])
                message = message.replace(sentence, f'{year}年{month}月')
            elif sentence in self.keyword_week.keys():  
                key_w = sentence
            elif sentence in self.week_list:
                self.key_week = self.week_list.index(sentence)
            elif sentence[:-1] in self.week_list:
                self.key_week = self.week_list.index(sentence[:-1])
        if key_w != None:
            diff = self.keyword_week[key_w]-(self.week-self.key_week)
            year, month, day = self.day_set(diff)
            if self.week_list[self.key_week]+'日' in message:
                message = message.replace(key_w,'')
                message = message.replace(self.week_list[self.key_week]+'日', f'{year}年{month}月{day}日')
            elif self.week_list[self.key_week] in message:
                message = message.replace(key_w,'')
                message = message.replace(self.week_list[self.key_week], f'{year}年{month}月{day}日')
            else:
                message = message.replace(key_w, f'{year}年{month}月{self.day}日')
        if diff_op:
            return message, diff
        return message
        
    # 日にちの変換
    def day_set(self,diff_num):
        update = self.now_date + timedelta(days = diff_num)
        return update.year,update.month,update.day
   
    # 月の変換
    def month_set(self, diff_num):
        year = self.year
        month = self.month
        if month + diff_num > 12:
            year += 1
            month = 1
        else:
            month += diff_num
        self.year = year
        self.month = month
        return year, month

if __name__ == '__main__':
    dup = Date_Update()
    s = input()
    a,diff = dup.convert(s,diff_op=True)
    print(a)
    print(diff)
    