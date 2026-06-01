from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class ServiceForm(FlaskForm): 
    serviceid = IntegerField('Szolgáltatás azonosítója', validators=[DataRequired()])
    name = StringField('Szolgáltatás neve', validators=[DataRequired()])
    price = IntegerField('Szolgáltatás ára', validators=[DataRequired()])
    submit_serupdate = SubmitField("Szolgáltatás módosítása")
    submit_seradd = SubmitField("Szolgáltatás hozzáadása")
    submit_serdelete = SubmitField("Szolgáltatás törlése")