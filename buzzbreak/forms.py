from flask_wtf import FlaskForm
from wtforms import SubmitField,PasswordField,StringField,ValidationError,BooleanField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo
from buzzbreak.models import User

class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired()])
    submit = SubmitField('Log In')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email Already Exists.')


class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(),Email()])
    password = PasswordField('Password:',validators=[DataRequired(),EqualTo('confirmpass',message="Password\'s must match")])
    confirmpass = PasswordField('Confirm Password:',validators=[DataRequired()])
    accept_tos  = BooleanField("I accpet the T&C",validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class AddPayOptForm(FlaskForm):
    payment_email = StringField("Payooner/Paypal Email address:",validators=[DataRequired(),Email()])
    submit = SubmitField("Add")

class VerifyPayOptForm(FlaskForm):
    payment_type = SelectField(
        'Verify Payment Type',
        validators=[DataRequired()],
        choices=[('Paypal','Paypal'),('Payoneer','Payoneer')]
    )
    submit = SubmitField('Update')

class AdminLogin(FlaskForm):
    admin_email = StringField("Admin Account:",validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('LOGIN')


class UpdatePayInfo(FlaskForm):
    read_payopt = StringField('Reading Payment:',validators=[DataRequired()])
    onclick_payopt = StringField('OnClick Payment:',validators=[DataRequired()])
    submit = SubmitField('UPDATE')