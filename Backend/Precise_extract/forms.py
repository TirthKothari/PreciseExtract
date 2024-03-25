from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from Precise_extract import mysql

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    # submit = SubmitField('Sign Up')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def validate_email(self,email):
    #     curr = mysql.connection.cursor()
    #     curr.execute("SELECT * FROM `user`")
    #     registerd_emails = curr.fetchall()
    #     print(registerd_emails)
    #     for e in registerd_emails:
    #          print(e[1])
    #          print(email.data)
    #          if email.data in e[1]:
    #             print("Email already registred")
    #             raise ValidationError('Email already registred')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password',validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')