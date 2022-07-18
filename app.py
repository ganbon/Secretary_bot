from flask import Flask, render_template
from flask import request
from flask_httpauth import HTTPBasicAuth
import sys
sys.path.append("..")
from system.chat import Chat
from config import id_list

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_pw(id):
    if id in id_list.keys():
        return id_list.get(id)
    else:
        return None
    
@app.route('/')
@app.route('/', methods = ['POST'])
@auth.login_required
def start_chat():    
    chat = Chat()  
    log = chat.start()
    user_message = request.form.get("send")
    if user_message != None:
        log = chat.run(user_message)
    return render_template("chat.html", chat_text = log)
    
if __name__ == '__main__':
    app.run(debug = True)