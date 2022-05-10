import subprocess
import webbrowser
import threading
import psutil
import os
from system.notice import Notice


class Command:
    def __init__(self):
        self.pid = []
        self.notice = Notice()
        
    def set_up(self):   
        webbrowser.open("http://127.0.0.1:5000/")

    def run(self, btn):
        self.callback(btn)
        command_anaconda = ['activate','deep']
        command_python = ['python','app.py']
        anaconda = subprocess.Popen(command_anaconda, shell = True)
        anaconda.communicate()
        python_file = subprocess.Popen(command_python, shell = True)
        python_file.communicate()
        
    def quit(self, btn):
        self.callback(btn)
        cwd=os.getcwd()
        for proc in psutil.process_iter():
            if 'python.exe'  in str(proc.exe) and cwd+'\\app.py' in proc.cmdline():
                self.pid.append(proc.pid)
            if self.pid != []:
                for p in self.pid:
                    command_quit = ['taskkill','/pid',str(p),'/F']
                    quit = subprocess.Popen(command_quit,shell=True)
                    quit.communicate()
                    self.pid=[]
                break
            else:
                continue
    
    def run_button_clicked(self, btn):
        run_thread = threading.Thread(target=self.run,args=(btn,),daemon=True)
        run_thread.start()

    def quit_button_clicked(self, btn):
        quit_thread = threading.Thread(target=self.quit,args=(btn,))
        quit_thread.start()
        
    def notice_run(self, btn):
        self.callback(btn)
        self.notice.run()
        
    def notice_button_clicked(self, btn):
        notice_thread = threading.Thread(target = self.notice_run, args = (btn,),daemon = True)
        notice_thread.start()
    
    def run_app_clicked(self):
        app_thread = threading.Thread(target = self.set_up)
        app_thread.start()
    
    def callback(self, btn):
        current_color = btn.cget('bg')
        if current_color == "#fef4f4":
            btn.config(bg = "#e6cde3")
        else:
            btn.config(bg = "#fef4f4")
    

    