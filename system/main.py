import MeCab
from datetime import datetime
import unicodedata
class A:
    def __init__(self):
        self.wakati=MeCab.Tagger("-Owakati")
        now_date=datetime.now()
        self.year=int(now_date.year)
        self.month=int(now_date.month)
        self.day=int(now_date.day)
        week_list=["月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日"]
        self.week=week_list[datetime.today().weekday()]
        self.hour=int(now_date.hour)
        self.minute=int(now_date.minute)
        self.date_word={"明日":str(self.day+1)+"日",
                        "明後日":str(self.day+2)+"日",
                        "来週":str(self.day+7)+"日",
                        "来月":str(self.month+1)+"月"} 
        
    def d_morpheme(self,input,speech=False):
        input=unicodedata.normalize('NFKC', input)
        if speech:
            speech_list=[]
            sentence = self.wakati.parse(input).split()
            node = self.wakati.parseToNode(input)
            while node:
                if node.feature.split(",")[0]!="BOS/EOS":
                    speech_list.append(node.feature.split(",")[0])    
                node=node.next
            return sentence,speech_list
        else:
            sentence=self.wakati.parse(input).split()
            return sentence
    
    #明日などの言い回しを日にちに変換
    def convert_date(self,input):
        word_list=self.d_morpheme(input)
        for w,word in enumerate(word_list):
            if word in list(self.date_word.keys()):
                word_list[w]=self.date_word[word]
        return ''.join(word_list)

a=A()
i=input()
b=a.d_morpheme(i,speech=True)
for s1,s2 in zip(b[0],b[1]):
    print(s1,s2)