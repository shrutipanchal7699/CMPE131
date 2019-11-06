from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
    
from app import login_manager
from app.forms import LoginForm, RegisterForm, QueryForm
from app.models import User, Room

from datetime import timedelta, date

def configure_routes(app):
    
    @app.route('/')
    def home_page():
        return render_template('home.html')


    @app.route('/auth', methods=['GET', 'POST'])
    def auth_page():
        if current_user.is_authenticated:
            return redirect(url_for('room_list_page'))

        login_form = LoginForm()
        register_form = RegisterForm()
        
        # Handles login form submissions
        if login_form.login_submit.data and login_form.validate():
            user = User.check_login(email=login_form.email.data, password=login_form.password.data)
            if user:
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('room_list_page'))
            else:
                login_form.raise_login_error()
                
        # Handles register form submissions
        if register_form.register_submit.data and register_form.validate():
            new_user = User.create(email=register_form.email.data, password=register_form.password.data)
            login_user(new_user)
            return redirect(url_for('room_list_page'))

        data = {
            'login_form': login_form,
            'register_form': register_form
        }

        return render_template('auth.html', **data)
    
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
        return render_template('reserve.html')
    
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
