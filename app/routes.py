from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user

from app import app, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User

#Set auth_page as the default login view for FlaskLogin
login_manager.login_view = 'auth_page'

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
        # Handles login form submission
        if login_form.login_submit.data and login_form.validate():
            user = User.check_login(email=login_form.email.data, password=login_form.password.data)
            if user:
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('room_list_page'))
            else:
                login_form.raise_login_error()
        # Handles register form submission
        if register_form.register_submit.data and register_form.validate():
            new_user = User.create(email=register_form.email.data, password=register_form.password.data)
            login_user(new_user)
            return redirect(url_for('room_list_page'))

        data = {
            'login_form': login_form,
            'register_form': register_form
        }

        return render_template('auth.html', **data)

    @app.route('/logout')
    def logout():
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('auth_page'))

    @app.route('/rooms')
    def room_list_page():
        return render_template('roomList.html')

    @app.route('/rooms/<id>')
    def room_detail_page(id):
        return render_template('roomDetail.html')

    @app.route('/rooms/<id>/book')
    def reserve_room_page(id):
        return render_template('reserve.html')

    @app.route('/bookings')
    def bookings_page():
        return render_template('bookings.html')

