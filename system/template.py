import csv
from datetime import datetime
import pandas as pd
from system.schedule_data import Schedule_Table
import googleapiclient.discovery
import google.auth 
import sys
import math
from setting import setting_load
sys.path.append('..')
from key.config import *
import moodle.data_get as md 


class Template(Schedule_Table):
    def __init__(self):
        super().__init__(csv_file_path = 'csv_data/schedule_2022.csv')
        self.log = None
        now_date = datetime.now()
        self.year = int(now_date.year)
        self.month = int(now_date.month)
        self.day = int(now_date.day)
        week_list = ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']
        self.week = week_list[datetime.today().weekday()]
        self.hour = int(now_date.hour)
        self.minute = int(now_date.minute)
        self.schedule_data = self.create_table()
        self.holiday_df = self.create_holiday()
        self.birth_month, self.birth_day, _, _, _ = setting_load()
        gapi_creds = google.auth.load_credentials_from_file(key, SCOPES)[0]
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials = gapi_creds)
        
    def log_load(self):
        with open('csv_data/chat_log.csv',mode = 'r',  encoding = 'utf8') as input_f:
            log = csv.reader(input_f)
            self.log_list = [o for o in log]
        return self.log_list
            
    def log_save(self):
        with open('csv_data/chat_log.csv',mode = 'w', encoding = 'utf8', newline = '') as input_f:
            write = csv.writer(input_f)
            write.writerows(self.log_list) 

    def inputlog_set(self,input):
        self.log_list.append([self.year, self.month, self.day, self.hour, self.minute, 'enc', input])

    def outputlog_set(self,output):
        self.log_list.append([self.year, self.month, self.day, self.hour, self.minute, 'dec', output])
        
    def start_chat(self):
        date_csv_data = [date[:3] for date in self.log_list]
        date_csv_data = [[int(d) for d in date] for date in date_csv_data]
        self.holiday_date()
        self.google_calender_get()
        if [self.year,self.month,self.day] not in date_csv_data or date_csv_data == []:
            self.moodle_plan()
            if self.hour < 12:
                out = 'おはようございます。'
            elif self.hour < 18:
                out = 'こんにちは。'
            else:
                out = 'こんばんは。'
            out += f'今日は{self.year}年{self.month}月{self.day}日{self.week}。\n'
            holiday = self.holiday_df[(self.holiday_df['月'] == self.month) & 
                                      (self.holiday_df['日'] == self.day) & 
                                      (self.holiday_df['年'] == self.year)]
            if holiday.empty:
                pass
            else:
                for h in holiday:
                    out+=f"{h}です。\n"
            if self.month==int(self.birth_month) and self.day==int(self.birth_day):
                out+='誕生日おめでとうございます🎂\n'
            out+= '今日の予定は'
            teach_csv_data = self.schedule_data[(self.schedule_data['月'] == self.month) & 
                                                (self.schedule_data['日'] == self.day) & 
                                                (self.schedule_data['年'] == self.year)]
            if teach_csv_data.empty:
                out += '特にありません。'
            else:
                for csv_data in teach_csv_data['予定']:
                    out += csv_data+'\n'
                out += 'です'
        else:
            out = None
        return out
    
    #祝日取得
    def holiday_date(self):
        holiday_list = self.holiday_df.values.tolist()
        now = datetime.utcnow().isoformat() + 'Z'
        try:
            req_holidays = self.service.events().list(calendarId = 'ja.japanese#holiday@group.v.calendar.google.com',
                                                  timeMin = now).execute()
        except ValueError:
            return
        holidays = req_holidays['items']
        def get_start_date(holiday):
            return holiday['start']['date']
        holidays.sort(key = get_start_date)
        for holiday in holidays:
            date = holiday['start']['date'].split('-')
            date = [int(x) for x in date]
            context = holiday['summary']
            date.append(context)
            if date not in holiday_list:
                self.update_holiday(date)

    #google calenderから予定取得
    def google_calender_get(self):
        schedule_list = self.frame_to_list()
        now = datetime.utcnow().isoformat() + 'Z'
        event_list = self.service.events().list(
            calendarId = calendar_id, timeMin = now,
            maxResults = 200, singleEvents = True,
            orderBy = 'startTime').execute()
        events = event_list.get("items", [])
        for event in events:
            date = event['start'].get('dateTime',event['start'].get('date'))
            context = event['summary']
            date = date.replace('T','-')
            date = date.replace('T','+')
            date = date.replace(':','-')
            date_list = date.split('-')
            
            if len(date_list) < 4:
                date_list = [int(x) for x in date_list] 
                date_list.append(None)
                date_list.append(None)
            else:
                date_list = date_list[:6]
                date_list = [int(x) for x in date_list]
            date_list.append(context)
            if date_list not in schedule_list:
                self.update_table(date)
    
    #moodle情報取得
    def moodle_plan(self):
        schedule_list = self.frame_to_list()
        html1, html2 = md.moodel_data()
        now_month = md.extract_html(html1)
        next_month = md.extract_html(html2)
        plan = now_month+next_month
        for p in plan:
            if p not in schedule_list:
                self.update_table(p)
                self.google_calender_register(p)
    
    def frame_to_list(self):
        schedule_list = self.schedule_data.values.tolist()
        for i,s_list in enumerate(schedule_list):
            for j,s in enumerate(s_list[:5]):
                if math.isnan(s):
                    schedule_list[i][j] = None
        return schedule_list