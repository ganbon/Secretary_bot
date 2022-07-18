from datetime import datetime
from nlptoolsjp.morpheme import morpheme
from nlptoolsjp.file_system import *
import unicodedata
import torch
import requests
from system.schedule import Discrimination
from system.summany import generate_text_from_model
import os
import re
import random
from setting import setting_load
from system.text_get import scraping
from system.emotion import generate


class Decoder(Discrimination):
    def __init__(self, message, csv_file_path = 'csv_data/schedule_2022.csv'):
        super().__init__(csv_file_path)
        self.message = unicodedata.normalize('NFKC', message)
        self.article_dir = 'text_data/'
        _, _, _, self.map_code, _ = setting_load()
        self.map_code = self.map_code.replace('\n','')
        self.bot_status = file_load('json_data/bot_status.json')
        self.url_pattern = "https?://[\w!?/+\-_~;.,*&@#$%()'[\]]+"
                
    #処理決定のための関数
    def decision(self):
        sentences = morpheme(self.message)
        out = ''
        #予定の登録
        if '記憶' in sentences or '覚え' in sentences:
            plan_data = self.schedule_register(self.message)
            if plan_data == 0:
                out = 'すみません。正確な日時を教えてくれませんか？'
                return out
            elif plan_data == -1:
                out = 'その予定はすでに登録されています。'
            else:
                if plan_data[3] == -1:
                    out = f'{plan_data[0]}年{plan_data[1]}月{plan_data[2]}日に{plan_data[5]}ですね。覚えておきます。'
                else:
                    out = f'{plan_data[0]}年{plan_data[1]}月{plan_data[2]}日{plan_data[3]}時{plan_data[4]}分に{plan_data[5]}ですね。覚えておきます。'            
        #指定した日程の予定を表示
        elif '予定' in sentences and ('教え' in sentences or '?' in sentences):
            month,day, plan_data = self.schedule_teach(self.message)
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
        elif ('削除' in sentences or '消し' in sentences or 'キャンセル' in sentences) and '予定' in sentences:
            record = self.schedule_get(self.message)
            if record.empty:
                out = '該当する予定が見つかりませんでした'
            else:
                self.schedule_delete(record)
                out = '予定を取り消しました'    
        #urlの内容を抽出して要約
        elif re.search(self.url_pattern,self.message) and '要約' in sentences:
            data_sum = sum(os.path.isfile(os.path.join(self.article_dir, name)) for name in os.listdir(self.article_dir))
            article_path = self.article_dir+'/text_data'+str(data_sum)+'.txt'
            url_oj = re.search(self.url_pattern,self.message)
            url = url_oj.group()
            try:
                scraping(url, article_path)
                summary_path = article_path
                generated_texts = generate_text_from_model(summary_path)
                for txt in generated_texts:
                    out += txt+'\n'
                out += 'テキスト内の文章を要約しました'
            except requests.exceptions.SSLError:
               out = 'すみません失敗しました' 
        #長文を1フレーズに要約
        elif '要約' in sentences:
            text = self.message.split(' ')[1]
            generated_texts = generate_text_from_model(text)
            for txt in generated_texts:
                    out += txt+'\n'
            out += 'url内の文章を取り出し要約しました'
        #webページをテキストファイルに変換
        elif '抽出' in sentences and re.search(self.url_pattern, self.message):
            data_sum = sum(os.path.isfile(os.path.join(self.article_dir, name)) for name in os.listdir(self.article_dir))
            article_path = self.article_dir+'/text_data'+str(data_sum)+'.txt'
            url_oj = re.search(self.url_pattern,self.message)
            url = url_oj.group()
            try:
                scraping(url, article_path)
                out = 'url内の記事を取り出しました'
            except requests.exceptions.SSLError:
               out = 'すみません失敗しました' 
        #曜日の確認
        elif '何曜日' in self.message:
            year, month, day,week = self.week_teach(self.message)
            if year == None:
                out = 'いつの話ですか？'
            else:   
                out = f'{year}年{month}月{day}日は{week}です。'
        #豆知識の表示
        elif '豆知識' in self.message and '教え' in self.message:
            knowledge = self.knowledge_teach()
            out = knowledge.replace('\n','')
        #天気予報の表示
        elif '天気' in sentences and ('教え' in sentences or '?' in sentences):
            plan_day,weather_data = self.weather_teach(self.message, self.map_code)
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
        #日本のTwitterにおける現在のトレンド上位10個を取得
        elif 'トレンド' in sentences and ('?' in sentences or '教え' in sentences):
            trends_list = self.twitter_trends_get()
            if trends_list == 0:
                out = 'キーが登録されてません。'
            out = '現在のトレンドは\n'
            for t,trend in enumerate(trends_list):
                t += 1
                out += f'{t}位:{trend}\n'
            out += 'です。'
        elif '起動' in sentences or '開い' in sentences:
            flg = self.app_start(sentences)
            if flg == 1:
                out = f'{sentences[0]}を起動しました。'
            else:
                out = f'起動できませんでした。'
        #該当しない入力の場合のときその言葉に対して感情表現をする
        else:
            random_date = datetime(self.year,self.month,self.day - 1,random.randint(0,23),random.randint(0,59))
            if datetime.strptime(self.bot_status['datetime'],'%Y-%m-%d %H:%M') < random_date:
                main_emotion = torch.zeros(5)
            self.bot_status['datetime'] = self.now_date.strftime('%Y-%m-%d %H:%M')
            main_emotion = self.bot_status['emotion']
            out, main_emotion = generate(self.message, main_emotion)
            self.bot_status['emotion'] = main_emotion
            file_create(self.bot_status,'json_data/bot_status.json')
        return out 