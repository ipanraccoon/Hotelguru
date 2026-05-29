from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class NewRoom(FlaskForm): 
    number = StringField('Szobaszám', validators=[DataRequired()])
    beds = IntegerField('Ágyak száma', validators=[DataRequired()])
    kitchen = BooleanField('Konyha')
    price = IntegerField('Ár egy éjszakára', validators=[DataRequired()])
    submit_add = SubmitField("Szoba hozzádás")