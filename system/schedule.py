import MeCab
import unicodedata
from datetime import  datetime
from system.date_update import Date_Update
from system.schedule_data import Schedule_Table
import datetime as dt
import math
import random

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
        self.date_key = ["年","月","日","時","分"]
        self.week = self.week_list[datetime.today().weekday()]
        self.hour = int(now_date.hour)
        self.minute = int(now_date.minute)

    #形態素解析
    def morpheme(self,input,speech=False):
        input=unicodedata.normalize('NFKC', input)
        if speech:
            speech_list = []
            sentence = self.wakati.parse(input).split()
            node = self.wakati.parseToNode(input)
            while node:
                if node.feature.split(",")[0] != "BOS/EOS":
                    speech_list.append(node.feature.split(",")[0])    
                node = node.next
            return sentence,speech_list
        else:
            sentence = self.wakati.parse(input).split()
            return sentence   
        
    #予定の内容抽出
    def content_extract(self,input_list,speech_list):
        out_list = []
        ban_word = ["覚え","記憶","予定"]
        for i,input in enumerate(input_list):
            if input in ban_word:
                break
            elif input.isdecimal() and input_list[i+1] in self.date_key:
                continue
            elif (input_list[i-1]).isdecimal() and input in self.date_key:
                continue
            elif out_list != [] and speech_list[i-1] == "名詞" and speech_list[i+1] == "名詞" and input_list[i+1] not in ban_word:
                out_list.append(input_list[i])
            elif speech_list[i] == "名詞":
                out_list.append(input)
            else:
                continue
        return ''.join(out_list)                
        
    #文章内の日程の取り出し
    def date_specify(self,date_kind,input_list):
        data = [input_list[i-1] for i,x in enumerate(input_list) if x == date_kind and input_list[i-1].isdecimal()]
        if data == []:
            return data
        else:
            return int(data[0])
    
    #予定の登録
    def schedule_register(self,input):
        schedule_list = self.schedule_date.values.tolist()
        for i,s_list in enumerate(schedule_list):
            for j,s in enumerate(s_list[:5]):
                if math.isnan(s):
                    schedule_list[i][j]=None
        input = self.date_update.convert(input)
        input_list,speech_list = self.morpheme(input,speech=True)
        plan_contents = self.content_extract(input_list,speech_list)
        plan_day = self.date_specify("日",input_list)
        plan_month = self.date_specify("月",input_list)
        plan_hour = self.date_specify("時",input_list)
        plan_hour = self.date_specify("時",input_list)
        plan_minute = self.date_specify("分",input_list)
        if plan_month == []:
            plan_month = self.month
        elif plan_hour == []:
            plan_hour = None
            plan_minute = None
        elif plan_hour != []:
            plan_minute = 0
        elif plan_day == []:
            return 0
        plan_data = [self.year,plan_month,plan_day,plan_hour,plan_minute,plan_contents]
        if plan_data in schedule_list:
            return -1
        self.schedule_date = self.update_table(plan_data)
        return plan_data
    
    #予定の受け渡し
    def schedule_teach(self,input):
        input = self.date_update.convert(input)
        input_list = self.morpheme(input,speech=False)
        teach_year = self.year
        teach_day = None
        data = self.schedule_date
        if "月" in input_list and "日" not in input_list:
            teach_month = self.date_specify("月",input_list)
            teach_data = data[(data["月"] == teach_month) & (data["年"] == teach_year)]
            return teach_month,teach_day,teach_data
        elif "日" in input_list and "月" not in input_list:
            teach_day = self.date_specify("日",input_list)
            teach_month = self.month
        elif "日" in input_list and "月" in input_list:
            teach_month = self.date_specify("月",input_list)
            teach_day = self.date_specify("日",input_list)
        teach_data = data[(data["月"] == teach_month) & (data["日"] == teach_day) & (data["年"] == teach_year)]
        return teach_month,teach_day,teach_data
    
    #予定の取り消し
    def delete_record(self, del_record):
        return super().delete_record(del_record)
    
    #特定のレコード取り出し   
    def schedule_get(self,input):
        input = self.date_update.convert(input)
        input_list = self.morpheme(input)
        day=self.date_specify("日",input_list)
        month=self.date_specify("月",input_list)
        plan = None
        #if day==[] or month==[]:
            #return 0
        plan_table = self.schedule_date[(self.schedule_date["月"]==month) & (self.schedule_date["日"]==day)]
        for p in plan_table["予定"]:
            if p in input:
                plan = p
        record = self.schedule_date[(self.schedule_date["月"] == month) & (self.schedule_date["日"] == day) & (self.schedule_date["予定"] == plan)]
        return record

    #曜日を教えてくれる
    def week_teach(self,input):
        year = None
        month = None
        day = None
        input = self.date_update.convert(input)
        input_list = self.morpheme(input)
        if "年" in input_list:
            year = self.date_specify("年",input_list)
        else:
            year = self.year
        if "月" in input_list:
            month = self.date_specify("月",input_list)
        else:
            month = self.month
        day = self.date_specify("日",input_list)
        d_key = dt.date(year,month,day)
        week_key = d_key.weekday()
        return year,month,day,self.week_list[week_key]
        
    #豆知識をランダムにわたす  
    def knowledge_teach(self):
        file_path = "text_data/min_kl.txt"
        with open(file_path,'r',encoding='UTF-8') as f:
            knowledge_data = f.readlines()
        knowledge = random.choice(knowledge_data)
        return knowledge 