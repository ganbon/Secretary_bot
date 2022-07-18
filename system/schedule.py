from nlptoolsjp.morpheme import morpheme
from nlptoolsjp.file_system import file_load
from datetime import datetime
from psutil import Popen
from system.date_update import Date_Update
from system.schedule_data import ScheduleTable
import re
import datetime as dt
import webbrowser
import requests
import random
import tweepy
from system.config import *


class Discrimination(ScheduleTable):
    def __init__(self, csv_file_path):  
        super().__init__(csv_file_path)
        self.schedule_date = self.create_table()
        self.date_update = Date_Update()
        self.now_date = datetime.now()
        self.year = int(self.now_date.year)
        self.month = int(self.now_date.month)
        self.day = int(self.now_date.day)
        self.week_list = ['月曜日','火曜日','水曜日','木曜日','金曜日','土曜日','日曜日']
        self.date_key = ['年','月','日','時','分']
        self.week = self.week_list[datetime.today().weekday()]
        self.hour = int(self.now_date.hour)
        self.minute = int(self.now_date.minute)   
        
    #予定の内容抽出
    def content_extract(self, input_dict):
        output_list = []
        sentences = list(input_dict.keys())
        speech_list = list(input_dict.values())
        ban_word = ['覚え','記憶']
        pass_word = ['予定','こと']
        for i,sentence in enumerate(sentences):
            if sentence in ban_word:
                break
            elif sentence in pass_word:
                continue
            elif sentence.isdecimal() and sentences[i+1] in self.date_key:
                continue
            elif sentences[i-1].isdecimal() and sentence in self.date_key:
                continue
            elif output_list != [] and speech_list[i-1]['speech'] == speech_list[i+1]['speech'] == '名詞' and sentences[i+1] not in pass_word:
                output_list.append(sentence)
            elif speech_list[i]['speech'] == '名詞':
                output_list.append(sentence)
            else:
                continue
        return ''.join(output_list)                
        
    #文章内の日程の取り出し
    def date_specify(self, date_kind, input_dict):
        if type(input_dict) is dict: 
            key_list = list(input_dict.keys())
        else:
            key_list = input_dict
        data = [key_list[i-1] for i,key in enumerate(key_list) if key == date_kind and key_list[i-1].isdecimal()]
        if data == []:
            return data
        else:
            return int(data[0])
    
    #予定の登録
    def schedule_register(self, message):
        schedule_list = self.schedule_date.values.tolist()
        message = self.date_update.convert(message)
        input_dict = morpheme(message,kind = True)
        plan_contents = self.content_extract(input_dict)
        plan_day = self.date_specify('日',input_dict)
        plan_month = self.date_specify('月',input_dict)
        plan_hour = self.date_specify('時',input_dict)
        plan_minute = self.date_specify('分',input_dict)
        if plan_month == []:
            plan_month = self.month
        if plan_hour == []:
            plan_hour = -1
            plan_minute = -1
        if plan_hour != [] and plan_minute == []:
            plan_minute = 0
        if plan_day == []:
            return 0
        plan_data = [self.year, plan_month, plan_day, plan_hour, plan_minute, plan_contents]
        if plan_data in schedule_list:
            return -1
        self.schedule_date = self.update_table(plan_data)
        self.google_calender_register(plan_data,'2')
        return plan_data
    
    #予定の受け渡し
    def schedule_teach(self, message):
        message = self.date_update.convert(message)
        sentences = morpheme(message, kind = False)
        teach_year = self.year
        teach_day = None
        data = self.schedule_date
        if '月' in sentences and '日' not in sentences:
            teach_month = self.date_specify('月',sentences)
            teach_data = data[(data['月'] == teach_month) & (data['年'] == teach_year)]
            return teach_month,teach_day,teach_data
        elif '日' in sentences and '月' not in sentences:
            teach_day = self.date_specify('日',sentences)
            teach_month = self.month
        elif '日' in sentences and '月' in sentences:
            teach_month = self.date_specify('月',sentences)
            teach_day = self.date_specify('日',sentences)
        teach_data = data[(data['月'] == teach_month) & (data['日'] == teach_day) & (data['年'] == teach_year)]
        return teach_month,teach_day,teach_data
    
    #特定のレコード取り出し   
    def schedule_get(self,message):
        message = self.date_update.convert(message)
        sentences = morpheme(message)
        day = self.date_specify('日',sentences)
        if day == []:
            day = self.day 
        month = self.date_specify('月',sentences)
        if month == []:
            month = self.month
        plan = None
        plan_table = self.schedule_date[(self.schedule_date['月'] == int(month)) 
                                        & (self.schedule_date['日'] == int(day))]
        for p in plan_table['予定']:
            if p in message:
                plan = p
        record = self.schedule_date[(self.schedule_date['月'] == int(month)) 
                                    & (self.schedule_date['日'] == int(day)) 
                                    & (self.schedule_date['予定'] == plan)]
        return record
    
    #予定の削除
    def schedule_delete(self, del_record):
        self.google_calender_delate(del_record)
        self.schedule_date = self.delete_record(del_record)
    
    #曜日の取得
    def week_teach(self,input):
        year = None
        month = None
        day = None
        input = self.date_update.convert(input)
        sentences = morpheme(input)
        if '年' in sentences:
            year = self.date_specify('年', sentences)
        else:
            year = self.year
        if '月' in sentences:
            month = self.date_specify('月', sentences)
        else:
            month = self.month
        day = self.date_specify('日', sentences)
        d_key = dt.date(year,month,day)
        week_key = d_key.weekday()
        return year,month,day,self.week_list[week_key]
        
    #豆知識をランダムにわたす  
    def knowledge_teach(self):
        file_path = 'text_data/min_kl.txt'
        knowledge_data = file_load(file_path)
        knowledge = random.choice(knowledge_data)
        return knowledge 
    
    #天気予報表示
    def weather_teach(self, messege, area):
        weather_data = []
        diff_day = 0
        plan_day = 0
        localmap_dict = file_load(file_path = 'json_data/localmap_data.json')
        area_list = list(localmap_dict.keys())
        messege, diff_day = self.date_update.convert(messege, diff_op = True)
        input_dict = morpheme(messege)
        plan_day = self.date_specify('日', input_dict)
        if abs(diff_day) > 2 or (plan_day == [] and diff_day != -1):
            return plan_day, weather_data
        if diff_day == -1:
            diff_day = 0
            plan_day = self.day
        for word in input_dict:
            if word in area_list:
                map_code = localmap_dict[word]
                if isinstance(map_code, list):
                    for _area in map_code:
                        code = localmap_dict[_area]
                        batch_data = self.weather_get(code, diff_day,_area)                          
                        weather_data.append(batch_data)
                else: 
                    batch_data = self.weather_get(map_code, diff_day, word)                          
                    weather_data.append(batch_data)
        #print(weather_data)
        if weather_data == []:
            try:
                batch_data = self.weather_get(localmap_dict[area], diff_day,area)
                weather_data.append(batch_data)
            except KeyError:
                return weather_data        
        return plan_day,weather_data
   
    #天気予報取得
    def weather_get(self,code,diff_day,word):
        weather_data = []
        url = 'https://weather.tsukumijima.net/api/forecast/city/' + code
        try:  
            response = requests.get(url)
            response.raise_for_status()
            weather_json = response.json()
            data = weather_json['forecasts'][diff_day]
            weather = data['telop']
            rain_data = data['chanceOfRain']
            weather_data = [word,weather, rain_data['T00_06'], rain_data['T06_12'], rain_data['T12_18'], rain_data['T18_24']]
            return weather_data
        except requests.exceptions.RequestException:
            return weather_data
    
    #Twitterのトレンド取得
    def twitter_trends_get(self):
        if len(API_Key) < 0 or len(API_Sec) < 0 or len(Token) < 0 or len(Token_Sec) < 0:
            return 0 
        auth = tweepy.OAuthHandler(API_Key, API_Sec)
        auth.set_access_token(Token, Token_Sec)
        api = tweepy.API(auth)
        #日本のWOEID
        woeid = 23424856
        trends = api.get_place_trends(woeid)
        trends_list = [t['name'] for t in trends[0]['trends'][:10]]
        return trends_list
    
    #登録したアプリ起動
    def app_start(self, sentence):
        path_dict = file_load(file_path='json_data/app_path_data.json')
        url_pattern = "https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+"
        for app_name in sentence:
            if app_name in path_dict:
                if re.match(url_pattern,path_dict[app_name]):
                    webbrowser.open(path_dict[app_name], 1)
                else:
                    Popen(path_dict[app_name])       
                return 1
            else:
                return 0
