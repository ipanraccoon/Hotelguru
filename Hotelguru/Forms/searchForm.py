from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField, DateField
from wtforms import validators
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    name = StringField('Név: ')
    city = StringField('Város: ')
    submit_search = SubmitField("Keresés")

class RoomSearchForm(FlaskForm):
    start_date = DateField('Érkezés', validators=[DataRequired()])
    end_date = DateField('Távozás', validators=[DataRequired()])
    submit_search = SubmitField("Szobák keresése")
