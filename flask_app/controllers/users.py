from flask_app.config.mysqlcontroller import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask_app.controllers import messages

bcrypt = Bcrypt(app)
OBFUSCATE_ID = lambda id: (id * 10000) + 83425
DE_OBFUSCATE = lambda ob_id: (int(ob_id) - 83425) / 10000

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard/' + str(OBFUSCATE_ID(session['user_id'])))
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pass_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pass_hash}
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard/' + str(OBFUSCATE_ID(session['user_id'])))

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user = User.get_user(request.form)
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email/password.')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard/' + str(OBFUSCATE_ID(session['user_id'])))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')