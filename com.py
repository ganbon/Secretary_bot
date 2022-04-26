import subprocess
import webbrowser
import threading
import psutil
class Comand:
    def __init__(self):
        self.pid=None
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
        for proc in psutil.process_iter():
            if 'python.exe'  in str(proc.exe) and 'app.py' in proc.cmdline()[1]:
                self.pid=proc.pid
            if self.pid  is not None:
                command_quit=['taskkill','/pid',str(self.pid),'/F']
                quit = subprocess.Popen(command_quit,shell=True)
                quit.communicate()
        
            
    def run_button_clicked(self):
        run_thread=threading.Thread(target=self.run)
        run_thread.start()

    def quit_button_clicked(self):
        quit_thread=threading.Thread(target=self.quit)
        quit_thread.start()