from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from app import login_manager
from app.forms import LoginForm, RegisterForm, QueryForm, MakeReservationForm
from app.models import User, Room, Reservation

from datetime import timedelta, date, datetime

def configure_routes(app):
    
    @app.route('/')
    def home_page():
        return redirect(url_for('room_list_page'))

    @app.route('/auth')
    @app.route('/auth/<form>')
    def auth_page(form=None):
        if current_user.is_authenticated:
            return redirect(url_for('room_list_page'))
        data = {
                'register_collapse': 'collapse',
                'login_collapse': 'collapse'
            }
        if form == 'login':
            data['login_collapse'] = 'collapse show'
        elif form == 'register':
            data['register_collapse'] = 'collapse show'
        return render_template('auth.html', **data)


    @app.route('/login', methods=['POST'])
    def login():
        f = LoginForm(data=request.form)
        if f.validate():
            #Login user
            login_user(f.valid_user, remember=f.remember.data)
            return redirect(url_for('room_list_page'))
        else:
            #put login errors in flash
            for field in f:
                for error in field.errors:
                    flash(str(error), 'login_' + field.name)
        return redirect(url_for('auth_page', form='login'))


    @app.route('/register', methods=['POST'])
    def register():
        f = RegisterForm(data=request.form)
        if f.validate():
            new_user = User.create(email=f.email.data, password=f.password.data)
            login_user(new_user)
            return redirect(url_for('room_list_page'))
        else:
            for field in f:
                for error in field.errors:
                    flash(str(error), 'register_' + field.name)
        return redirect(url_for('auth_page', form='register'))

    #User logout 
    @app.route('/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('auth_page'))


    #displays list of rooms to the user
    @app.route('/rooms', methods=['GET', 'POST'])
    def room_list_page():
        return render_template('roomList.html')

    @app.route('/fetch_rooms')
    def fetch_room_list():
        cleaned_data = {
            'csrf_token': request.args.get('csrf_token'),
            'check_in_date' : datetime.strptime(request.args.get('check_in_date'), '%Y-%m-%d').date(),
            'check_out_date' : datetime.strptime(request.args.get('check_out_date'), '%Y-%m-%d').date(),
            'num_occupants' : int(request.args.get('num_occupants')),
            'room_type' : request.args.get('room_type')
        }

        f = QueryForm(data=cleaned_data)
        if f.validate():
            rooms = Room.fetch_room_to_query(cleaned_data)
            return render_template('roomSearchResults.html', rooms=rooms)
        else:
            print(f.errors.items())
        return "Hello"

    # displays the details of different rooms
    @app.route('/rooms/<id>')
    def room_detail_page(id):
        return render_template('roomDetail.html')

    #for user reservation
    @app.route('/rooms/<id>/book')
    def reserve_room_page(id):
        form = MakeReservationForm()
        return render_template('reserve.html', form = form)
    
    #Bookings Page
    @app.route('/bookings')
    @login_required
    def bookings_page():
        reservations = Reservation.fetch_users_reservation(current_user.id)
        data = {
            'reservations' : reservations
        }
        return render_template('bookings.html', **data)
    
    #CancelReservation Page
    @app.route('/bookings/<res_id>/cancel')
    @login_required
    def cancel_reservation(res_id):
        """
        res_id: id of reservation the client wants to cancel
        """
        current_user.delete_reservation(res_id)
        return redirect(url_for('bookings_page'))
