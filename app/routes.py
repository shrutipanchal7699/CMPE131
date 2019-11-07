from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
    
from app import login_manager
from app.forms import LoginForm, RegisterForm, QueryForm, MakeReservationForm
from app.models import User, Room

from datetime import timedelta, date

def configure_routes(app):
    
    @app.route('/')
    def home_page():
        return render_template('home.html')


    @app.route('/auth')
    def auth_page():
        if current_user.is_authenticated:
            return redirect(url_for('room_list_page'))

        return render_template('auth.html')


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
        return redirect(url_for('auth_page'))


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
        return redirect(url_for('auth_page'))

    #User logout 
    @app.route('/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('auth_page'))

    #displays list of rooms to the user
    @app.route('/rooms', methods=['GET', 'POST'])
    def room_list_page():
        query = {
            'check_in_date': date.today() + timedelta(days = 1),
            'check_out_date': date.today() + timedelta(days = 6)
        }
        rooms = []
        form = QueryForm()
        if form.validate_on_submit():
            rooms = Room.fetch_room_to_query({
                'check_in_date': form.check_in_date.data,
                'check_out_date': form.check_out_date.data,
                'room_type': form.room_type.data,
                'num_occupants': form.number_of_occupants.data
            })
        return render_template('roomList.html', form=form, rooms=rooms)

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
        return render_template('bookings.html', data)
    
    #CancelReservation Page
   #@app.route('/cancellation')
   #def cancellation_page():
        #return render_template('cancelReservation.html')
        
    #ViewReservations Page
   #@app.route('/view')
   #def viewReservation_page():
        #return render_template('viewReservation.html')
