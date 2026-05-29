from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class NewHotel(FlaskForm): 
    name = StringField('Név', validators=[DataRequired()])
    city = StringField('Város', validators=[DataRequired()])
    address = StringField('Cím', validators=[DataRequired()])
    submit_add = SubmitField("Hotel hozzáadása")

class UpdateHotel(FlaskForm):
    hotelid = IntegerField('Hotel id', validators=[DataRequired()])
    name = StringField('Név', validators=[DataRequired()])
    address = StringField('Cím', validators=[DataRequired()])
    city = StringField('Város', validators=[DataRequired()])
    submit_update = SubmitField("Hotel módosítása")

class DeleteHotel(FlaskForm): 
    hotelid = IntegerField('Hotel id', validators=[DataRequired()])
    submit_delete = SubmitField("Hotel törlés")