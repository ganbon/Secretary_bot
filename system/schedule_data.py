import pandas as pd
from datetime import datetime
class Schedule_Table:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.clumns = ["年","月","日","時","分","予定"]
        self.df = None
        self.header = False
    
    #チャットログを読み込む
    def create_table(self):
        try:
            df = pd.read_csv(self.csv_file_path, names = self.clumns)
        except FileNotFoundError:
            df = pd.DataFrame([], columns = self.clumns)
        self.df = df
        self.expired_record()
        return df

    #更新
    def update_table(self, update_date):
        self.df.loc[len(self.df)] = update_date
        self.df.to_csv("csv_data/schedule_2022.csv",mode = 'w',index = False,header = False)
        return self.df

    #すでに過ぎた予定を削除
    def expired_record(self):
        now_date = datetime.now()
        now_month = int(now_date.month)
        now_day = int(now_date.day)
        delete_data = self.df[(self.df['月'] <= now_month) & (self.df['日'] < now_day)]
        print(delete_data)
        self.delete_record(delete_data)
            
    #予定を削除
    def delete_record(self, del_record):
        for index,data in del_record.iterrows():
            self.df.drop(index,inplace = True)
        self.df.to_csv("csv_data/schedule_2022.csv",mode = 'w',index = False,header = False)

'''        
import math
import pprint
s=Schedule_Table("../csv_data/schedule_2022.csv")
a=s.create_table()
b=a.values.tolist()
for i,s_list in enumerate(b):
            for j,s in enumerate(s_list[:5]):
                if math.isnan(float(s)):
                    b[i][j]=None
pprint.pprint(b)
pprint.pprint(a)
print(b[4][3])
print(float('nan'))
print(math.isnan(float(b[4][3])))
if [2022,5,7,float('nan'),float('nan'),'テスト'] in b:
    print(2)
''' 