import tkinter as tk
from com import Command

com = Command()
root = tk.Tk()
root.title("秘書チャット")
root.geometry("350x300")
root.config(bg='#eaf4fc')
run_button = tk.Button(root, text="アプリ起動", width = 20, font = ('MSゴシック',17),
                       fg = '#223a70', bg = '#fef4f4', command = lambda:com.run_button_clicked(run_button))
run_button.pack()
app_button = tk.Button(root, text = "アプリ表示", width = 20, font = ('MSゴシック',17),
                       fg = '#223a70', bg = '#fef4f4', command = com.set_up)
app_button.pack()
quit_button = tk.Button(root, text = "アプリ停止", width = 20,font = ('MSゴシック',17),
                        fg = '#223a70', bg = '#fef4f4', command = lambda:com.quit_button_clicked(run_button))
quit_button.pack()
notice_button = tk.Button(root, text="通知機能", width=20, font=('MSゴシック',17),
                          fg = '#223a70', bg='#fef4f4', command = lambda:com.notice_button_clicked(notice_button))
notice_button.pack()
root.iconbitmap(default = "app.ico")
root.mainloop()
