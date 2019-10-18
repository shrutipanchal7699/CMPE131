from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
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
    email = StringField(
        'email', 
        validators=[InputRequired(),Length(max=50)]
        )

    password = PasswordField(
        'password', 
        validators=[InputRequired(), Length(max=80)]
        )
    remember = BooleanField('remember me')
    login_submit = SubmitField('Login')

    def raise_login_error(self):
        self.password.errors = [ValidationError('Invalid login information')]

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

    register_submit = SubmitField('Register')

