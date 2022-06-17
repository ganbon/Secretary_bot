import pandas as pd
from datetime import datetime
import googleapiclient.discovery
import google.auth 
import sys
sys.path.append('..')
from key.config import *


class Schedule_Table:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.clumns = ['年','月','日','時','分','予定']
        self.hol_clumns = ['年','月','日','内容']
        self.df = None
        self.header = False
        self.holiday_df = None
        gapi_creds = google.auth.load_credentials_from_file(key, SCOPES)[0]
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials = gapi_creds)
    
    #予定データを読み込む
    def create_table(self):
        try:
            df = pd.read_csv(self.csv_file_path, names = self.clumns)
            df.astype = {'年':int,'月':int,'日':int,'時':int,'分':int,"予定":str}
        except FileNotFoundError:
            df = pd.DataFrame([], columns = self.clumns)
            df.astype = {'年':int,'月':int,'日':int,'時':int,'分':int,"予定":str}
        self.df = df
        self.expired_record()
        return df

    #更新
    def update_table(self, update_date):
        print(update_date)
        self.df.loc[len(self.df)] = update_date
        self.df.to_csv('csv_data/schedule_2022.csv', mode = 'w', index = False, header = False)
        return self.df

    #すでに過ぎた予定を削除
    def expired_record(self):
        now_date = datetime.now()
        now_month = int(now_date.month)
        now_day = int(now_date.day)
        delete_data = self.df[(self.df['月'] <= now_month) & (self.df['日'] < now_day)]
        self.delete_record(delete_data)
            
    #予定を削除
    def delete_record(self, del_record):
        for index,data in del_record.iterrows():
            self.df.drop(index,inplace = True)
        self.df.to_csv('csv_data/schedule_2022.csv', mode = 'w', index = False, header = False)
    
    def create_holiday(self):
        try:
            self.holiday_df = pd.read_csv('csv_data/holiday.csv', names = self.hol_clumns)
            self.holiday_df.astype = {'年':int,'月':int,'日':int,"内容":str}
        except FileNotFoundError:
            self.holiday_df = pd.DataFrame([], columns = self.hol_clumns)
            self.holiday_df.astype = {'年':int,'月':int,'日':int,"内容":str}
        return self.holiday_df
    
    def update_holiday(self,update_data):
        self.holiday_df.loc[len(self.holiday_df)] = update_data
        self.holiday_df.to_csv('csv_data/holiday.csv', mode = 'w', index = False, header = False)

    #googlecalenderに予定追加
    def google_calender_register(self,plan_data):
        year, month, day, hour, minute, plan = plan_data
        if hour == -1:
            event= {
                    # 予定のタイトル
                    'summary': plan,
                    # 予定の開始時刻(ISOフォーマットで指定)
                    'start': {
                        'date': f'{year}-{month}-{day}',
                        'timeZone': 'Japan'
                    },
                    # 予定の終了時刻(ISOフォーマットで指定)
                    'end': {
                        'date': f'{year}-{month}-{day}',
                        'timeZone': 'Japan'
                    },
                }
        else:
            start_hour = hour
            end_hour = hour+1
            event= {
                    # 予定のタイトル
                    'summary': plan,
                    # 予定の開始時刻(ISOフォーマットで指定)
                    'start': {
                        'date': f'{year}-{month}-{day}-{start_hour}-{minute}',
                        'timeZone': 'Japan'
                    },
                    # 予定の終了時刻(ISOフォーマットで指定)
                    'end': {
                        'date': f'{year}-{month}-{day}-{end_hour}-{minute}',
                        'timeZone': 'Japan'
                    },
                }
        event = self.service.events().insert(calendarId = calendar_id, body = event).execute()
