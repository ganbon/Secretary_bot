from system.decoder import Decoder
from system.template import Template
from system.notice import Notice

class Chat:
    def __init__(self):
        self.tmplate = Template()
        #self.notice = Notice()
        
    #チャットの初期設定
    def start(self):
        log_list = self.tmplate.log_load()
        tmp_out = self.tmplate.start_chat()
        if tmp_out != None:
            self.tmplate.outputlog_set(tmp_out)
            self.tmplate.log_save()
        return log_list
    
    
    #実装
    def run(self,input):
        log_list=self.tmplate.log_load()    
        #self.notice.run()
        decorder = Decoder(input)
        output = decorder.decision()
        self.tmplate.inputlog_set(input)
        self.tmplate.outputlog_set(output)    
        self.tmplate.log_save()
        log_list = self.tmplate.log_load()
        return log_list
        
        
