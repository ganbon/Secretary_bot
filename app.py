from flask import Flask, render_template
from flask import request
import sys
sys.path.append("..")
from system.chat import Chat

app = Flask(__name__)
@app.route('/')

@app.route('/', methods = ['POST'])
def start_chat():    
    chat = Chat()  
    log = chat.start()
    input = request.form.get("send")
    if input != None:
        log = chat.run(input)
    return render_template("chat.html", chat_text = log)
    
if __name__ == '__main__':
    app.run(debug = True)