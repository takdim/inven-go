from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ingat Saya')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=50, message='Username harus 3-50 karakter')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nama_lengkap = StringField('Nama Lengkap', validators=[
        DataRequired(),
        Length(min=3, max=255, message='Nama lengkap harus 3-255 karakter')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password minimal 6 karakter')
    ])
    password2 = PasswordField('Konfirmasi Password', validators=[
        DataRequired(),
        EqualTo('password', message='Password tidak cocok')
    ])
    submit = SubmitField('Daftar')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username sudah digunakan. Silakan pilih username lain.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email sudah terdaftar. Silakan gunakan email lain.')
