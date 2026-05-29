from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email, length

class RegisterForm(FlaskForm): 
    name = StringField('Név', validators=[DataRequired()])
    phone = StringField('Telefonszám', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField("Jelszó", validators=[DataRequired(), length(min=6)])
    submit_register = SubmitField("Regisztráció")
    