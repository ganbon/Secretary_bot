from datetime import datetime, time,timedelta
from plyer import notification
import time 
from system.schedule_data import Schedule_Table
from setting import setting_load

class Notice:
    def __init__(self):
        self.schedule = Schedule_Table(csv_file_path = 'csv_data/schedule_2022.csv')
        _, _, _, _, self.step = setting_load()
                
    def run(self):
        set_hour = [x for x in range(0, 24, int(self.step))]
        while(1):
            self.plan_data = self.schedule.create_table()
            now_date = datetime.now()
            period_date = now_date + timedelta(days = 6)
            period_month = int(period_date.month)
            period_day = int(period_date.day)
            now_month = int(now_date.month)
            now_day = int(now_date.day)
            now_hour = int(now_date.hour)
            now_minute = int(now_date.minute)
            if now_hour in set_hour and now_minute == 6:
                if now_month == period_month:
                    plan_df = self.plan_data[(self.plan_data['月'] == now_month) & 
                                         ((self.plan_data['日'] > now_day) | (period_day > self.plan_data['日']))]
                else:
                    plan_df = self.plan_data[((self.plan_data['月'] == now_month) & ((self.plan_data['日'] > now_day))
                                             | (self.plan_data['月'] == period_month) & ((self.plan_data['日'] < period_day)))]
                for index,data in plan_df.iterrows():
                    self.display(data)
                time.sleep(60)

    def display(self, task):
        year, month, day, hour,minute,data = task
        if hour == -1:
            nt_messege = f'{int(month)}月{int(day)}日に{data}の予定があります。'
        else:
            nt_messege = f'{int(month)}月{int(day)}日{int(hour)}時{int(minute)}分に{data}があります。'
        notification.notify(
            title = '秘書からのお知らせ',
            message = nt_messege,
            app_name = '秘書チャット',
            app_icon = 'image/app.ico',
            timeout = 10
        )
        