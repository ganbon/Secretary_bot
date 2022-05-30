from system.decoder import Decoder
from system.template import Template
import subprocess
import threading
import time

class Chat:
    def __init__(self):
        self.tmplate = Template()
        
    #チャットの初期設定
    def start(self):
        log_list = self.tmplate.log_load()
        tmp_out = self.tmplate.start_chat()
        if tmp_out != None:
            self.tmplate.outputlog_set(tmp_out)
            self.tmplate.log_save()
            yukkuri_thread = threading.Thread(target = self.yukkuri, args=(tmp_out,))
            yukkuri_thread.start()
        return log_list
    
    #実装
    def run(self, input):
        log_list = self.tmplate.log_load()    
        decorder = Decoder(input)
        output = decorder.decision()
        self.tmplate.inputlog_set(input)
        self.tmplate.outputlog_set(output)    
        self.tmplate.log_save()
        log_list = self.tmplate.log_load()
        yukkuri_thread = threading.Thread(target = self.yukkuri, args=(output,))
        yukkuri_thread.start()
        return log_list
    
    def yukkuri(self, word, active = True):
        convert_word = {'😊':'えへへへ','😲':'えっほんと？','😞':'寂しいよ','😧':'うわーーん','🙂':'なるほど','😡':'は？'}
        if word in convert_word:
            word = convert_word[word]
        speak = word.replace('\n','')
        _start = 'softalk\\SofTalk.exe'
        _speed = '/S:100'
        start_com = [_start, _speed, '/X:1', f'/W:{speak}']
        endcom = ['softalk\\SofTalk.exe','/close_now']
        if active:
            start = subprocess.Popen(start_com, shell = True)
            time.sleep(20)
            end = subprocess.Popen(endcom, shell = True)