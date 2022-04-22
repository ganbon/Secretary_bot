from system.decorder import Decorder
from system.template import Template

class Chat:
    def __init__(self):
        self.tmplate=Template()
    
    def start(self):
        log_list=self.tmplate.log_load()
        tmp_out=self.tmplate.start_chat()
        if tmp_out!=None:
            self.tmplate.outputlog_set(tmp_out)
            self.tmplate.log_save()
        return log_list
    
    
    def run(self,input):
        log_list=self.tmplate.log_load()    
        decorder=Decorder(input)
        output=decorder.decision()
        self.tmplate.inputlog_set(input)
        self.tmplate.outputlog_set(output)    
        self.tmplate.log_save()
        log_list=self.tmplate.log_load()
        return log_list
        
        
