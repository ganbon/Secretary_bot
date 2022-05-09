from datetime import datetime, time
import math
from plyer import notification
import pandas as pd
import time
from system.schedule_data import Schedule_Table

class Notice:
    def __init__(self):
        schedule=Schedule_Table(csv_file_path="csv_data/schedule_2022.csv")
        self.plan_data=schedule.create_table()
                
    def run(self):
        while(1):
            now_date = datetime.now()
            now_month = int(now_date.month)
            now_day = int(now_date.day)
            now_hour = int(now_date.hour)
            now_minute = int(now_date.minute)
            set_hour = [8,12,16,17,20]
            if now_hour in set_hour and now_minute == 34:
                plan_df = self.plan_data[(self.plan_data['月'] >= now_month) & (self.plan_data['日'] > now_day+1) | (now_day+7 > self.plan_data['日'])]
                print(plan_df)
                for index,data in plan_df.iterrows():
                    self.display(data)
                time.sleep(60)

    def display(self,task):
        for i,s in enumerate(task[:5]):
                if math.isnan(s):
                    task[i] = None
        year, month, day, hour,minute,data = task
        if hour == None:
            nt_messege = f'{month}月{day}日に{data}の予定が入ってあります。'
        else:
            nt_messege = f'{month}月{day}日{hour}時{minute}分に{data}の予定が入ってあります。'
        notification.notify(
            title = "秘書からのお知らせ",
            message = nt_messege,
            app_name = "秘書チャット",
            app_icon = "image2.ico",
            timeout = 10
        )