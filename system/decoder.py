import MeCab
import unicodedata
import requests
from system.schedule import Discrimination
from system.summany import generate_text_from_model
import os
import re
from system.text_get import scraping
from system.emotion import generate
class Decoder(Discrimination):
    def __init__(self, input, csv_file_path = 'csv_data/schedule_2022.csv'):
        super().__init__(csv_file_path)
        self.wakati = MeCab.Tagger('-Owakati')
        self.input = unicodedata.normalize('NFKC', input)
        self.article_dir = 'text_data/'
        self.map_code='高松'
        self.url_pattern="https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+"
                
    #処理決定のための関数
    def decision(self):
        sentences = self.morpheme(self.input)
        #覚えておいてほしい予定を覚えててくれる 
        if '記憶' in sentences or '覚え' in sentences:
            plan_data = self.schedule_register(self.input)
            if plan_data == 0:
                out='すみません。正確な日時を教えてくれませんか？'
                return out
            elif plan_data == -1:
                out='その予定はすでに登録されています。'
            else:
                if plan_data[3] == None:
                    out = f'{plan_data[0]}年{plan_data[1]}月{plan_data[2]}日に{plan_data[5]}ですね。覚えておきます。'
                else:
                    out = f'{plan_data[0]}年{plan_data[1]}月{plan_data[2]}日{plan_data[3]}時{plan_data[4]}分に{plan_data[5]}ですね。覚えておきます。'            
        #指定した日程の予定を教えてくれる
        elif '予定' in sentences and ('教え' in sentences or '?' in sentences):
            month,day,plan_data = self.schedule_teach(self.input)
            if plan_data.empty:
                out = '予定は特にありません。'
            else:
                if day is None:
                    out = str(month)+'月の予定は\n'
                    for d,plan in zip(plan_data['日'],plan_data['予定']):
                        out += str(d)+'日に'+plan+'\n'
                else:
                    out = str(month)+'月'+str(day)+'日の予定は\n'
                    for plan in plan_data['予定']:
                        out+=plan+'\n'
                out += 'です。'   
        #予定のキャンセル
        elif ('削除' in sentences or '消し' in sentences) and '予定' in sentences:
            record = self.schedule_get(self.input)
            #if (record==0).all():
                #out = 'うまく処理ができませんでした。正確な日にちを入力してください'
            if record.empty:
                out = '該当する予定が見つかりませんでした'
            else:
                self.delete_record(record)
                out = '予定を取り消しました'    
        #urlの内容を抽出して要約
        elif '抽出' in sentences and re.search(self.url_pattern,self.input) and '要約' in sentences:
            data_sum = sum(os.path.isfile(os.path.join(self.article_dir, name)) for name in os.listdir(self.article_dir))
            article_path = self.article_dir+'/text_data'+str(data_sum)+'.txt'
            url_oj = re.search(self.url_pattern,self.input)
            url = url_oj.group()
            try:
                scraping(url, article_path)
                summary_path = article_path
                generated_texts = generate_text_from_model(summary_path)
                out = generated_texts[0]
                out += '\nurl内の記事を取り出し要約しました'
            except requests.exceptions.SSLError:
               out = 'すみません失敗しました' 
        #長文を1フレーズに要約
        elif '要約' in sentences:
            text = self.input.split(' ')[1]
            generated_texts = generate_text_from_model(text)
            out = generated_texts[0]
        #webページをテキストファイルに変換
        elif '抽出' in sentences and re.search(self.url_pattern, self.input):
            data_sum = sum(os.path.isfile(os.path.join(self.article_dir, name)) for name in os.listdir(self.article_dir))
            article_path = self.article_dir+'/text_data'+str(data_sum)+'.txt'
            url_oj = re.search(self.url_pattern,self.input)
            url = url_oj.group()
            try:
                scraping(url, article_path)
                out = 'url内の記事を取り出しました'
            except requests.exceptions.SSLError:
               out = 'すみません失敗しました' 
        #曜日の確認
        elif '何曜日' in self.input:
            year,month,day,week = self.week_teach(self.input)
            if year == None:
                out = 'いつの話ですか？'
            else:   
                out = f'{year}年{month}月{day}日は{week}です。'
        #豆知識教えてくれる
        elif '豆知識' in self.input and '教え' in self.input:
            knowledge = self.knowledge_teach()
            out = knowledge.replace('\n','')
        #該当しない入力の場合のときその言葉に対して感情表現をする
        elif '天気' in sentences and ('教え' in sentences or '?' in sentences):
            plan_day,weather_data = self.weather_teach(self.input, self.map_code)
            if weather_data == []:
                out = '天気の取得に失敗しました。'
            else:
                out=f'{plan_day}日は\n'
                for i,weather in enumerate(weather_data):
                    area,ws,rain_data1,rain_data2,rain_data3,rain_data4 = weather
                    if len(weather_data) > 1:
                        out += f'{area}が{ws}。\n降水確率が0~6時{rain_data1}、6～12時{rain_data2}、12～18時{rain_data3}、18～24時{rain_data4}'
                    else:
                        out += f'{ws}。\n降水確率が0~6時{rain_data1}、6～12時{rain_data2}、12～18時{rain_data3}、18～24時{rain_data4}'
                    if len(weather_data) > 1:
                        out += '\n'
                out += 'です。'
        #該当しない入力の場合のときその言葉に対して感情表現をする
        else:
            out = generate(self.input)
        return out