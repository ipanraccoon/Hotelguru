from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    city = StringField('Város', validators=[DataRequired()])
    submit_search = SubmitField("Keresés")
