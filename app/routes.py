from flask import render_template, redirect, url_for

from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def homePage():
    return render_template('home.html')

@app.route('/auth', methods=['GET', 'POST'])
def authPage():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        print(login_form.validate())
        return login_form.username.data + ' ' + login_form.password.data

    if register_form.validate_on_submit():
        return register_form

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
