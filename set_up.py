import tkinter as tk
import sys
from com import Command

com=Command()
root=tk.Tk()
root.title("秘書チャット")
root.geometry("280x240")
run_button=tk.Button(root,text="サーバ起動",width=30,command=com.run_button_clicked)
run_button.pack()
quit_button=tk.Button(root,text="サーバ停止",width=30,command=com.quit_button_clicked)
quit_button.pack()
app_button=tk.Button(root,text="アプリ起動",width=30,command=com.set_up)
app_button.pack()


root.mainloop()

