from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField
from wtforms import validators
from wtforms.validators import DataRequired, Email, length

class ReserveForm(FlaskForm): 
    roomid = SelectMultipleField('Válasszon szobákat', coerce=int, validators=[DataRequired()])
    submit_reservation = SubmitField("Foglal")
    