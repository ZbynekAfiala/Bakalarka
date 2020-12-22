from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from myproject.models import User

class LoginForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(),Email()])
    password = PasswordField('Heslo:',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(),Email()])
    username = StringField('Uživatelské jméno:',validators=[DataRequired()])
    password = PasswordField('Heslo:',validators=[DataRequired(),EqualTo('password_confirm',message='Hesla musí být shodná !')])
    password_confirm = PasswordField('Potvrďte heslo:', validators=[DataRequired()])
    submit = SubmitField('Registrovat!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Tento email je už registrován.')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Toto uživatelské jméno již existuje.')

class UpdateUserForm(FlaskForm):
    email = StringField('Email:',validators=[DataRequired(),Email()])
    username = StringField('Uživatelské jméno', validators=[DataRequired()])
    picture = FileField('Aktualizovat profilový obrázek',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Aktualizovat')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Tento email je už registrován.')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Toto uživatelské jméno již existuje.')
