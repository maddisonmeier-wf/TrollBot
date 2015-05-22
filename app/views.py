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
    
    new_message = request.args.get('usermsg')
    
    if not new_message:
        return render_template('chat_bot.html',
                                title='Office Bot',
                                name='office_bot')

    

    return_message = analyze_input(new_message)
    app.logger.info(return_message)
    