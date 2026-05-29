from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email, length

class UpdateForm(FlaskForm): 
    name = StringField('Név', validators=[DataRequired()])
    phone = StringField('Telefonszám', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired()])
    submit = SubmitField("Adatok módosítása", validators=[DataRequired()])
    