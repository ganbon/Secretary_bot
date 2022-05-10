import csv
from datetime import datetime
import pandas as pd
from system.schedule_data import Schedule_Table

class Template(Schedule_Table):
    def __init__(self):
        super().__init__(csv_file_path="csv_data/schedule_2022.csv")
        self.log = None
        now_date = datetime.now()
        self.year = int(now_date.year)
        self.month = int(now_date.month)
        self.day = int(now_date.day)
        week_list = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]
        self.week = week_list[datetime.today().weekday()]
        self.hour = int(now_date.hour)
        self.minute = int(now_date.minute)
        self.schedule_csv_data = self.create_table()
        
    def log_load(self):
        with open("csv_data/chat_log.csv",mode = "r",encoding = "utf8") as input_f:
            log = csv.reader(input_f)
            self.log_list = [o for o in log]
        return self.log_list
            
    def log_save(self):
        with open("csv_data/chat_log.csv",mode = "w",encoding = "utf8",newline = "") as input_f:
            write = csv.writer(input_f)
            write.writerows(self.log_list) 

    def inputlog_set(self,input):
        self.log_list.append([self.year,self.month,self.day,self.hour,self.minute,"enc",input])

    def outputlog_set(self,output):
        self.log_list.append([self.year,self.month,self.day,self.hour,self.minute,"dec",output])
        
    def start_chat(self):
        day_csv_data = [int(day[2]) for day in self.log_list]
        if self.day not in day_csv_data or day_csv_data == []:
            if 5 < self.hour < 12:
                out = "おはようございます。"
            elif 12 <= self.hour < 18:
                out = "こんにちは。"
            else:
                out = "こんばんは。"
            out += f"今日は{self.year}年{self.month}月{self.day}日{self.week}です。\n今日の予定は"
            teach_csv_data = self.schedule_csv_data[(self.schedule_csv_data["月"] == self.month) & (self.schedule_csv_data["日"] == self.day) & (self.schedule_csv_data["年"] == self.year)]
            if teach_csv_data.empty:
                out += "特にありません。"
            else:
                for csv_data in teach_csv_data["予定"]:
                    out += csv_data+"\n"
                out += "です"
        else:
            out = None
        return out

        
        