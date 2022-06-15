import tkinter as tk
from com import Command
from sub_app import SubApp, Op_App
from PIL import Image,ImageTk
splash = tk.Tk()
gif_index = 0

def next_frame():
    global gif_index
    try:
        # XXX: 次のフレームに移る
        photo.configure(format="gif -index {}".format(gif_index))

        gif_index += 1
    except tk.TclError:
        gif_index = 0
        return next_frame()
    else:
        splash.after(100, next_frame)
        
splash.overrideredirect(1)  # スプラッシュ画面のタイトルバー非表示
ww = splash.winfo_screenwidth()  
wh = splash.winfo_screenheight()  
image = Image.open('image/loading.gif')
w,h = image.size
splash.geometry(f"{w}x{h}+{ww//4}+{wh//8}")
photo = tk.PhotoImage(file="image/loading.gif")  # 表示させたい画像ファイル指定

canvas = tk.Canvas(bg = "white", width = w, height = h)  
canvas.place(x=0, y=0)
canvas.create_image(0, 0, image = photo, anchor = tk.NW)
splash.after_idle(next_frame)

def main():
    splash.destroy()
    op = Op_App()
    com = Command()
    sub = SubApp()
    root = tk.Tk()
    root.title('秘書チャット')
    root.geometry('350x300')
    root.config(bg='#eaf4fc')
    img = ImageTk.PhotoImage(file='image/app.ico')
    root.tk.call('wm', 'iconphoto', root._w, img)
    run_button = tk.Button(root, text = 'アプリ起動', width = 20, font = ('MSゴシック', 17),
                        fg='#223a70', bg = '#fef4f4', command = lambda: com.app_switch(run_button))
    app_button = tk.Button(root, text = 'アプリ表示', width = 20, font=('MSゴシック', 17),
                        fg='#223a70', bg = '#fef4f4', command = com.display_app_clicked)
    notice_button = tk.Button(root, text = '通知ON', width = 20, font = ('MSゴシック', 17),
                        fg='#223a70', bg = '#fef4f4', command = lambda: com.notice_switch(notice_button))
    text_bar_button = tk.Button(root, text = 'サブアプリ表示', width = 20, font = ('MSゴシック', 17),
                        fg='#223a70', bg = '#fef4f4', command = sub.text_bar)
    detail_button = tk.Button(root, text = "詳細設定", width = 20, font = ('MSゴシック', 17),
                        fg='#223a70', bg='#fef4f4', command = op.setting_display)
    run_button.pack()
    app_button.pack()
    notice_button.pack()
    text_bar_button.pack()
    detail_button.pack()
    pid_list = com.find_process([('app.py', 1), ('notice_active.py', 0)])
    if pid_list['app.py'] != -1:
        run_button.config(bg='#e6cde3')
        run_button.config(text='アプリ停止')

    if pid_list['notice_active.py'] != -1:
        notice_button.config(bg='#e6cde3')
        notice_button.config(text='通知OFF')
splash.after(5000,main)
tk.mainloop()