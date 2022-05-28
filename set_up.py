import tkinter as tk
from com import Command

com = Command()
root = tk.Tk()
root.title('秘書チャット')
root.geometry('350x300')
root.config(bg='#eaf4fc')
run_button = tk.Button(root, text = 'アプリ起動', width = 20, font = ('MSゴシック', 17),
                       fg = '#223a70', bg = '#fef4f4', command = lambda:com.app_switch(run_button))
run_button.pack()
app_button = tk.Button(root, text = 'アプリ表示', width = 20, font = ('MSゴシック', 17),
                       fg = '#223a70', bg = '#fef4f4', command = com.display_app_clicked)
app_button.pack()
notice_button = tk.Button(root, text = '通知ON', width = 20, font = ('MSゴシック', 17),
                          fg = '#223a70', bg = '#fef4f4', command = lambda:com.notice_switch(notice_button))
notice_button.pack()
root.iconbitmap(default = 'app.ico')
if com.find_process('app.py') != []:
    run_button.config(bg = '#e6cde3')
    run_button.config(text = 'アプリ停止')
    
if com.find_process('notice_active.py') != []:
    notice_button.config(bg = '#e6cde3')
    notice_button.config(text = '通知OFF')
root.mainloop()
