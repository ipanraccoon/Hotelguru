from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class DeleteRoom(FlaskForm): 
    roomid = IntegerField('Szoba id', validators=[DataRequired()])
    submit_delete = SubmitField("Szoba törlés")