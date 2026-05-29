from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class UpdateRoom(FlaskForm): 
    number = StringField('Szobaszám', validators=[DataRequired()])
    beds = IntegerField('Ágyak száma', validators=[DataRequired()])
    kitchen = BooleanField('Konyha')
    price = IntegerField('Ár egy éjszakára', validators=[DataRequired()])
    roomid = IntegerField('Szoba id', validators=[DataRequired()])
    submit_update = SubmitField("Szoba módosítás")