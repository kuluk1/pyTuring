# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, SubmitField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo

# USer model
from app.mod_auth.models import User


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email    = TextField('Email Address', [Email(),
                Required(message='Must provide an email.')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])
    submit = SubmitField('submit')

class RegisterForm(FlaskForm):
    username = TextField('Username', [Required(message='Must provide an username.')])
    email    = TextField('Email Address', [Email(),
                Required(message='Must provide an email.')])
    password = PasswordField('Password', [
                Required(message='Must provide a password.')])
    submit = SubmitField('submit')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Select a differente username')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Select a different email')
