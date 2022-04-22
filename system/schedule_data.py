import pandas as pd

class Schedule_Table:
    def __init__(self,csv_file_path):
        self.csv_file_path = csv_file_path
        self.clumns = ["年","月","日","時","分","予定"]
        self.df = None
        self.header = False
    
    #チャットログを読み込む
    def create_table(self):
        try:
            df = pd.read_csv(self.csv_file_path,names=self.clumns)
        except FileNotFoundError:
            df = pd.DataFrame([],columns = self.clumns)
        self.df = df
        return df

    #更新
    def update_table(self,update_date):
        self.df.loc[len(self.df)] = update_date
        self.df.to_csv("csv_data/schedule_2022.csv",mode = 'w',index = False,header = False)
        return self.df

    def delete_record(self,del_record):
        self.df.drop(del_record)
        
        
'''        
s=Schedule_Table("../csv_data/schedule_2022.csv")
a=s.create_table()
teach_data=a[(a["月"]==4)&(a["年"]==2022)]
print(teach_data)
print(teach_data["月"][0])
'''   
        

        
