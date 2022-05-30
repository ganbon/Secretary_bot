import subprocess
import webbrowser
import threading
import psutil
import os
import itertools
from system.notice import Notice


class Command:
    def __init__(self):
        self.notice = Notice()
        
    def set_up(self):   
        webbrowser.open('http://127.0.0.1:5000/', 1)

    def run(self ,file_name):
        command_anaconda = ['activate', 'deep']
        command_python = ['python', file_name]    
        anaconda = subprocess.Popen(command_anaconda, shell = True)
        anaconda.communicate()
        self.python_file = subprocess.Popen(command_python, shell = True)
        self.python_file.communicate()
        
    def quit(self, file_name,p_type):
        pid = self.find_process([(file_name, p_type)])
        if pid[file_name] != -1:
            command_quit = ['taskkill','/pid',str(pid[file_name]),'/F']
            quit = subprocess.Popen(command_quit, shell = True)
            quit.communicate()
            print('停止しました')
        else:
            pass

    def find_process(self, file_name = []):
        cwd = os.getcwd()
        pid_list = {}
        pro_list = [proc for proc in psutil.process_iter() if 'python.exe' in str(proc.exe)]
        for name, proc in itertools.product(file_name, pro_list):
            f_name, p_type = name
            if f'{cwd}\\{f_name}' in proc.cmdline() and p_type == 1:
                pid_list[f_name] = proc.pid
            elif f_name in proc.cmdline() and p_type == 0:
                pid_list[f_name] = proc.pid
            elif f_name not in pid_list:
                pid_list[f_name] = -1;
        return pid_list
    
    def app_switch(self, btn):
        run_app_thread = threading.Thread(target = self.run, args = ('app.py',))
        quit_app_thread = threading.Thread(target = self.quit, args = ('app.py',1))
        if btn.cget('bg') == '#fef4f4':
            run_app_thread.start()
            btn.config(text = 'アプリ起動')
            self.callback(btn)
        else:
            quit_app_thread.start()
            btn.config(text = 'アプリ停止')
            self.callback(btn)
        
    def notice_switch(self, btn):
        run_notice_thread = threading.Thread(target = self.run, args = ('notice_active.py',))
        quit_notice_thread = threading.Thread(target = self.quit, args = ('notice_active.py',0))
        if btn.cget('bg') == '#e6cde3':
            quit_notice_thread.start()
            btn.config(text = '通知ON')
            self.callback(btn)
            return   
        else:
            run_notice_thread.start()
            self.callback(btn)
            btn.config(text = '通知OFF')
        
    def display_app_clicked(self):
        self.app_thread = threading.Thread(target = self.set_up)
        self.app_thread.start()
    
    def callback(self, btn):
        current_color = btn.cget('bg')
        if current_color == '#fef4f4':
            btn.config(bg = '#e6cde3')
        else:
            btn.config(bg = '#fef4f4')