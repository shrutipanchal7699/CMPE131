from flask import render_template

from app import app


@app.route('/')
def homePage():
    return render_template('home.html')

@app.route('/auth')
def authPage():
    return render_template('auth.html')

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
