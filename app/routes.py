from flask import render_template, redirect, url_for

from app import app, db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_user, current_user

@app.route('/')
def homePage():
    return render_template('home.html')

#Set authPage as the default login view for FlaskLogin
login_manager.login_view = 'authPage'

@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.login_submit.data and login_form.validate():
        user = User.check_login(email=login_form.email.data, password=login_form.password.data)
        if user:
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('roomListPage'))

    if register_form.register_submit.data and register_form.validate():
        new_user = User.create(email=register_form.email.data, password=register_form.password.data)
        login_user(new_user)
        return redirect(url_for('roomListPage'))

    data = {
        'login_form': login_form,
        'register_form': register_form
    }

    return render_template('auth.html', **data)

@app.route('/rooms')
def roomListPage():
    return render_template('roomList.html')

@app.route('/rooms/<id>')
def roomDetailPage(id):
    return render_template('roomDetail.html')

@app.route('/rooms/<id>/book')
def reserveRoomPage(id):
    return render_template('reserve.html')

@app.route('/bookings')
def bookingsPage():
    return render_template('bookings.html')
