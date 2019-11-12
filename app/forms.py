import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from app.models import User

class Unique(object):
    """ validator that checks field uniqueness """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

class LoginForm(FlaskForm):

    valid_user = None

    email = StringField(
        'email', 
        validators=[InputRequired(),Length(max=50)]
        )

    password = PasswordField(
        'password', 
        validators=[
            InputRequired(),
            Length(max=80),
            ]
        )
    remember = BooleanField('remember me')

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        
        user = User.check_login(email=self.email.data, password=self.password.data)
        if user:
            self.valid_user = user
            return True
        else:
            self.password.errors = [ValidationError('Invalid login information')]
            return False

class RegisterForm(FlaskForm):
    email = StringField(
        'email', 
        validators=[
            InputRequired(), 
            Email(message='Invalid Email'), 
            Length(max=50),
            Unique(User, User.email, 'Email is already in use')])

    password = PasswordField(
        'password', 
        validators=[
            InputRequired(),
            Length(min=8, max=80),
            EqualTo('confirm', message='Passwords must match')])

    confirm  = PasswordField('Repeat Password')

class QueryForm(FlaskForm):
    check_in_date = DateField('Check In Date')

    check_out_date = DateField('Check Out Date')

    room_type = SelectField(choices=[
        ('Regular','Regular'),
        ('Executive','Executive'),
        ('President','President')
    ])

    num_occupants = IntegerField('Number of Occupants')

    def validate(self):
        #Both dates are not in the past
        res = super(QueryForm, self).validate()
        if self.check_in_date.data < datetime.date.today():
            self.raise_date_in_past_error(self.check_in_date)
            return False
        if self.check_out_date.data < datetime.date.today():
            self.raise_date_in_past_error(self.check_out_date)
            return False
        #Start date has to be earlier than end date
        if self.check_in_date.data > self.check_out_date.data:
            self.raise_start_after_end_error()
            return False

        return res and True

    def raise_date_in_past_error(self, field):
        field.errors = [ValidationError("Date can't be in the past")]
    
    def raise_start_after_end_error(self):
        self.check_in_date.errors = [ValidationError("Start date can't come after end date")]


class MakeReservationForm(FlaskForm):
    check_in_date = DateField(
        'Check In Date',
        validators = [
            InputRequired()
            ]
    )

    check_out_date = DateField(
        'Check Out Date',
        validators = [
            InputRequired()
            ]
    )

    room_type = SelectField('Room Type', choices=[
        ('Regular','Regular'),
        ('Executive','Executive'),
        ('President','President')],
         validators = [
            InputRequired()
            ]

    )

    number_of_occupants = IntegerField(
        'Number of Occupants',
         validators = [
            InputRequired()
            ]
    )

    def validate(self):
        #Both dates are not in the past
        res = super(QueryForm, self).validate()
        if self.check_in_date.data < date.today():
            self.raise_date_in_past_error(self.check_in_date)
            return False
        if self.check_out_date.data < date.today():
            self.raise_date_in_past_error(self.check_out_date)
            return False
        #Start date has to be earlier than end date
        if self.check_in_date.data > self.check_out_date.data:
            self.raise_start_after_end_error()
            return False

        return res and True

    def raise_date_in_past_error(self, field):
        field.errors = [ValidationError("Date can't be in the past")]
    
    def raise_start_after_end_error(self):
        self.check_in_date.errors = [ValidationError("Start date can't come after end date")]