from calendar import weekday
import MeCab
import unicodedata
from datetime import  datetime
from system.date_update import Date_Update
from system.schedule_data import Schedule_Table
import datetime as dt


class Discrimination(Schedule_Table):
    def __init__(self,csv_file_path):
        super().__init__(csv_file_path)
        self.schedule_date = self.create_table()
        self.wakati = MeCab.Tagger("-Owakati")
        self.date_update = Date_Update()
        now_date = datetime.now()
        self.year = int(now_date.year)
        self.month = int(now_date.month)
        self.day = int(now_date.day)
        self.week_list = ["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]
        self.week = self.week_list[datetime.today().weekday()]
        self.hour = int(now_date.hour)
        self.minute = int(now_date.minute)

    #形態素解析
    def d_morpheme(self,input,speech=False):
        input=unicodedata.normalize('NFKC', input)
        if speech:
            speech_list = []
            sentence = self.wakati.parse(input).split()
            node = self.wakati.parseToNode(input)
            while node:
                if node.feature.split(",")[0] != "BOS/EOS":
                    speech_list.append(node.feature.split(",")[0])    
                node=node.next
            return sentence,speech_list
        else:
            sentence=self.wakati.parse(input).split()
            return sentence   
        
    #予定の内容抽出
    def content_extract(self,input_list,speech_list):
        out_list = []
        for i,input in enumerate(input_list):
            if input == "覚え" or input == "記憶":
                break
            elif input.isdecimal():
                continue
            elif (input_list[i-1]).isdecimal() and (input == "年",input == "月" or input == "日" or input == "時" or input == "分"):
                continue
            elif out_list == [] and speech_list[i-1] == "助詞" and speech_list[i] == "名詞":
                out_list.append(input_list[i])
            elif out_list != [] and speech_list[i-1] == "名詞" and speech_list[i+1] == "名詞":
                out_list.append(input_list[i])
            elif speech_list[i] == "名詞" and (input=="こと" or input=="予定"):
                out_list.append(input)
            else:
                continue
        return ''.join(out_list)                
        
    #文章内の日程の取り出し
    def date_specify(self,date_kind,input_list):
        data=[input_list[i-1] for i,x in enumerate(input_list) if x == date_kind and input_list[i-1].isdecimal()]
        return data[0]
    
    #予定の登録
    def schedule_register(self,input):
        input = self.date_update.convert(input)
        input_list,speech_list = self.d_morpheme(input,speech=True)
        plan_contents = self.content_extract(input_list,speech_list)
        if "日" in input_list and "月" in input_list and "時" in input_list:
            plan_day = int(self.date_specify("日",input_list))
            plan_month = int(self.date_specify("月",input_list))
            plan_hour = int(self.date_specify("時",input_list))
            if "分" in input_list:
                plan_minute = int(self.date_specify("分",input_list))
            else:
                plan_minute = 0
        elif "日" in input_list and "月" not in input_list and "時" in input_list:
            plan_day = int(self.date_specify("日",input_list))
            plan_month = self.month
            plan_hour = int(self.date_specify("時",input_list))
            if "分" in input_list:
                plan_minute = int(self.date_specify("分",input_list))
            else:
                plan_minute = 0
        elif "日" in input_list and "月" not in input_list:
            plan_day = int(self.date_specify("日",input_list))
            plan_month = self.month
            plan_hour = None
            plan_minute = None
        elif "日" in input_list and "月" in input_list:
            plan_day = int(self.date_specify("日",input_list))
            plan_month = int(self.date_specify("月",input_list))
            plan_hour = None
            plan_minute = None
        else:
            return 0
        plan_data = [self.year,plan_month,plan_day,plan_hour,plan_minute,plan_contents]
        self.schedule_date = self.update_table(plan_data)
        return plan_data
    
    #予定の受け渡し
    def scedule_teach(self,input):
        input = self.date_update.convert(input)
        input_list = self.d_morpheme(input,speech=False)
        teach_year = self.year
        teach_day = None
        data = self.schedule_date
        if "月" in input_list and "日" not in input_list:
            teach_month = int(self.date_specify("月",input_list))
            teach_data = data[(data["月"] == teach_month) & (data["年"] == teach_year)]
            return teach_month,teach_day,teach_data
        elif "日" in input_list and "月" not in input_list:
            teach_day = int(self.date_specify("日",input_list))
            teach_month = self.month
        elif "日" in input_list and "月" in input_list:
            teach_month = int(self.date_specify("月",input_list))
            teach_day = int(self.date_specify("日",input_list))
        teach_data = data[(data["月"] == teach_month) & (data["日"] == teach_day) & (data["年"] == teach_year)]
        return teach_month,teach_day,teach_data
    
    #予定の取り消し
    def delete_record(self, del_record):
        return super().delete_record(del_record)
    
    #特定のレコード取り出し   
    def scedule_get(self,input):
        input = self.date_update.convert(input)
        input_list = self.d_morpheme(input)
        month = self.month
        day = self.day
        plan = None
        for ipt in input_list:
            if ipt in self.schedule_date["月"]:
               month = ipt
            if ipt in self.schedule_date["予定"]:
                plan = ipt
        record = self.schedule_date[(self.schedule_date["月"] == month) & (self.schedule_date["日"] == day) & (self.schedule_date["予定"] == plan)]
        return record
    

    def teach_week(self,input):
        year = None
        month = None
        day = None
        input = self.date_update.convert(input)
        input_list = self.d_morpheme(input)
        if "年" in input_list:
            year = int(self.date_specify("年",input_list))
        else:
            year = self.year
        if "月" in input_list:
            month = int(self.date_specify("月",input_list))
        else:
            month = self.month
        day = int(self.date_specify("日",input_list))
        d_key = dt.date(year,month,day)
        week_key = d_key.weekday()
        return year,month,day,self.week_list[week_key]
        
        