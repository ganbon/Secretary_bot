import tkinter as tk
from system.chat import Chat
import tkinter.ttk as ttk
from setting import setting_load,setting_save
from com import Command

class SubApp:
    def __init__(self):
        self.txt = None

    def text_bar(self):
        app1 = tk.Tk()
        app1.config(bg = '#eaf4fc')
        hight = app1.winfo_screenheight()
        width = app1.winfo_screenwidth()
        app1.geometry(f'500x50+{width-500}+{hight-200}')
        self.txt = tk.Entry(app1, width = 30, font = ('MSゴシック' ,15))
        self.txt.grid(column = 0, row = 0, pady = 10, padx = 10)
        send_button =  tk.Button(app1, text = '送信', width = 10, font = ('MSゴシック', 15),
                            fg = '#223a70', bg = '#fef4f4', command = self.send)
        send_button.grid(column = 1, row = 0, pady = 10, padx = 10)
        app1.attributes('-topmost', True)
        app1.mainloop()
    
    def send(self):
        chat = Chat()
        input = self.txt.get()
        log = chat.start()
        log = chat.run(input)
        self.txt.delete(0, tk.END)


class Op_App:
    def __init__(self):
        self.com = Command()
    
    def setting_display(self,flg = 0):
        app2 = tk.Tk()
        if flg == 0:
            month, day, self.voice, area_name, notition_time = setting_load()
        app2.config(bg = '#eaf4fc')
        app2.geometry('300x300')
        frame1 = tk.Frame(app2)
        frame2 = tk.Frame(app2)
        frame3 = tk.Frame(app2)
        frame4 = tk.Frame(app2)
        frame1.pack(pady = 5)
        frame2.pack(pady = 5)
        frame3.pack(pady = 5)
        hour_list = [x for x in range(1,6)]
        month_list = [x for x in range(1,13)]
        day_list = [x for x in range(1,31)]
        notice_time_label = tk.Label(frame1, text = '通知間隔',
                                     font = ('MSゴシック', 15, 'bold'))
        notice_time = ttk.Combobox(frame1, width = 2,
                         values = hour_list, state = 'readonly',
                         font = ('MSゴシック', 10, 'bold'))
        hour_label = tk.Label(frame1, text = '時間',
                                     font = ('MSゴシック', 10, 'bold'))
        notice_time_label.grid(row = 0, column = 0)
        notice_time.set(notition_time)
        notice_time.grid(row = 0, column = 1)
        hour_label.grid(row = 0, column = 2)
        area_label = tk.Label(frame2, text = '地域',
                                     font = ('MSゴシック', 15, 'bold'))
        area = tk.Entry(frame2, width = 7, font = ('MSゴシック' ,15, 'bold'))
        area.insert(0, area_name)
        area_label.grid(row = 0, column = 0)
        area.grid(row = 0, column = 1)
        birth_label = tk.Label(frame3, text = '誕生日',
                                     font = ('MSゴシック', 15, 'bold'))
        month_label = tk.Label(frame3, text = '月',
                                     font = ('MSゴシック', 10, 'bold'))
        day_label = tk.Label(frame3, text = '日',
                                     font = ('MSゴシック', 10, 'bold'))
        birth_month = ttk.Combobox(frame3, width = 2,
                         values = month_list, state = 'readonly',
                         font = ('MSゴシック', 10, 'bold'))
        birth_month.set(month)
        birth_day = ttk.Combobox(frame3, width = 2,
                         values = day_list, state = 'readonly',
                         font = ('MSゴシック', 10, 'bold'))
        birth_day.set(day)
        birth_label.grid(row = 0, column = 0)
        birth_month.grid(row = 0, column = 1)
        month_label.grid(row = 0,column = 2)
        birth_day.grid(row = 0, column = 3)
        day_label.grid(row = 0,column = 4)
        voice_button = tk.Button(app2, text = 'ボイスON', width = 20, font = ('MSゴシック', 17),
                       fg = '#223a70', bg = '#fef4f4',command = lambda: self.voice_switch(voice_button))
        if flg == 0 and int(self.voice) == 1:
            self.com.callback(voice_button,"ボイスOFF")
        flg = 1
        voice_button.pack(pady = 5)
        self.setting_data = [birth_month, birth_day, self.voice, area, notice_time]
        print(self.setting_data)
        send_button =  tk.Button(frame4, text = '決定', width = 10, font = ('MSゴシック', 15),
                            fg = '#223a70', bg = '#fef4f4', command = lambda: setting_save(self.setting_data, app2))
        exit_button =  tk.Button(frame4, text = 'キャンセル', width = 10, font = ('MSゴシック', 15),
                            fg = '#223a70', bg = '#fef4f4', command = app2.destroy)
        send_button.grid(row = 0, column = 0)
        exit_button.grid(row = 0, column = 1)
        frame4.pack(pady = 5)
        app2.mainloop()
    
    def voice_switch(self, btn):
        if int(self.voice) == 0:
            self.com.callback(btn, 'ボイスOFF')
            self.voice = 1
        else:
            self.com.callback(btn, 'ボイスON')
            self.voice = 0
        self.setting_data[2] = str(self.voice)
