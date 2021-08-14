from flask_app.config.mysqlcontroller import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.message import Message
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from datetime import datetime, date

OBFUSCATE_ID = lambda id: (id * 10000) + 83425
DE_OBFUSCATE = lambda ob_id: (int(ob_id) - 83425) / 10000

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    if session['user_id'] != DE_OBFUSCATE(user_id):
        return redirect('/')
    user = User.get_user(session)
    targets = User.get_all_users()
    messages = Message.get_messages_with_author({'target_id': session['user_id']})
    num_sent = len(Message.get_messages_with_author({'user_id': session['user_id']}, user_or_target='user_id'))
    num_recieved = len(messages)
    now = datetime.now()
    for message in messages:
        seconds =  (now - message['created_at']).seconds
        minutes = int(seconds/60)
        hours = int(minutes/60)
        days = int(hours/24)
        if days > 0:
            message['time_since'] = f'Sent {days} days ago.'
        elif hours > 0:
            message['time_since'] = f'Sent {hours} hours ago.'
        else:
            message['time_since'] = f'Sent {minutes} minutes ago.'
        
    return render_template('dashboard.html', user=user, targets=targets, messages=messages[::-1], num_sent=num_sent,
                            num_recieved=num_recieved)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect('/')
    data = {'user_id': int(session['user_id']),
            'target_id': int(request.form['target']),
            'content': request.form['message']}
    Message.send_message(data)
    return redirect('/dashboard/' + str(OBFUSCATE_ID(int(session['user_id']))))