import subprocess
import webbrowser
import threading
import psutil
import os
import ctypes
from system.notice import Notice


class Command:
    def __init__(self):
        self.pid_list = []
        self.notice = Notice()
        
    def set_up(self):   
        webbrowser.open('http://127.0.0.1:5000/', 1)

    def run(self):
        command_anaconda = ['activate', 'deep']
        command_python = ['python', 'app.py']    
        anaconda = subprocess.Popen(command_anaconda, shell = True)
        anaconda.communicate()
        self.python_file = subprocess.Popen(command_python, shell = True)
        self.python_file.communicate()
        
    def quit(self, file_name):
        self.pid_list = self.find_process(file_name)
        if self.pid_list != []:
            for p in self.pid_list:
                command_quit = ['taskkill','/pid',str(p),'/F']
                quit = subprocess.Popen(command_quit, shell=True)
                quit.communicate()
                print('停止しました')
            self.pid_list = []
        else:
            pass

    def find_process(self, file_name):
        cwd = os.getcwd()
        pid_list = []
        for proc in psutil.process_iter():
            if 'python.exe' in str(proc.exe) and f'{cwd}\\{file_name}' in proc.cmdline():
                pid_list.append(proc.pid)
        return pid_list
    
    def app_switch(self, btn):
        self.run_app_thread = threading.Thread(target = self.run)
        self.quit_app_thread = threading.Thread(target = self.quit,args = ('app.py',))
        self.callback(btn)
        if btn.cget('bg') == '#fef4f4':
            btn.config(text = 'アプリ起動')
            self.quit_app_thread.start()
        else:
            btn.config(text = 'アプリ停止')
            self.run_app_thread.start()
        
    def notice_switch(self, btn):
        if btn.cget('bg') == '#e6cde3':
            btn.config(text = '通知ON')
            self.callback(btn)
            native_id = self.notice_thread.native_id
            ctypes.pythonapi.PyThreadState_SetAsyncExc(native_id, ctypes.py_object(SystemExit))
            print("通知機能停止")
            return   
        else:
            self.notice_thread = threading.Thread(target = self.notice.run)
            self.callback(btn)
            btn.config(text = '通知OFF')
            self.notice_thread.start()
        
    def display_app_clicked(self):
        self.app_thread = threading.Thread(target = self.set_up)
        self.app_thread.start()
    
    def callback(self, btn):
        current_color = btn.cget('bg')
        if current_color == '#fef4f4':
            btn.config(bg = '#e6cde3')
        else:
            btn.config(bg = '#fef4f4')