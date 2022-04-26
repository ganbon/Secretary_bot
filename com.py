import subprocess
import webbrowser
import threading
import psutil
import os
class Comand:
    def __init__(self):
        self.pid=[]
    def set_up(self):   
        webbrowser.open("http://127.0.0.1:5000/")

    def run(self):
        command_anaconda = ['activate','deep']
        command_python = ['python','app.py']
        anaconda = subprocess.Popen(command_anaconda,shell=True)
        anaconda.communicate()
        python_file = subprocess.Popen(command_python,shell=True)
        python_file.communicate()
        

    def quit(self):
        cwd=os.getcwd()
        print(cwd)
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
            
    def run_button_clicked(self):
        run_thread=threading.Thread(target=self.run,daemon=True)
        run_thread.start()

    def quit_button_clicked(self):
        quit_thread=threading.Thread(target=self.quit)
        quit_thread.start()