from flask import render_template, request
from app import app
from cli_chat import analyze_input

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='ChatBot',
                           user=user)

@app.route('/office_bot', methods=['GET', 'POST'])
def office_bot():
    
    if request.method == 'GET':
        return render_template('chat_bot.html',
                                title='Office Bot',
                                name='office_bot')



    return analyze_input(request.form['text'])
    