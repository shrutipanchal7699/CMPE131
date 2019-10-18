from flask import render_template, redirect, url_for
from werkzeug import generate_password_hash

from app import app, db
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route('/')
def homePage():
    return render_template('home.html')

@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.login_submit.data and login_form.validate():
        print('POSTED LOGIN FORM')
        return login_form.email.data + ' ' + login_form.password.data

    if register_form.register_submit.data and register_form.validate():
        pw_hash = generate_password_hash(register_form.password.data)
        new_user = User.create(email=register_form.email.data, password_hash=pw_hash)
        return 'New User created!' + new_user.email

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
