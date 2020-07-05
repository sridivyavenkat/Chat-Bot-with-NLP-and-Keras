from flask import Flask
from flask import render_template, request, redirect, url_for
from flask import jsonify
from gui import send
from gtts import gTTS
import os


app = Flask(__name__)


@app.route('/chat/', methods=['POST'])
def chat():
    text = request.form['text']
    res = ""
    if text != "":
        res = send(text)
        t_res = res['repley']
        file_name = "static/music/" + t_res[:4] + '.mp3'
        if os.path.isfile(file_name):
            os.remove(file_name)
        tts = gTTS(text=t_res, lang='en')
        tts.save(file_name)
    return jsonify({'response': res['repley'], 'options': res['options'], 'file_name': file_name})


@app.route('/', methods=['POST', 'GET'])
def home1():
    return render_template('page.html')


if __name__ == '__main__':
    app.run(debug=True)
