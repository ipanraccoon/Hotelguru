from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class RoomForm(FlaskForm):
    roomid =  IntegerField('Room ID')
    number = StringField('Szobaszám', validators=[DataRequired()])
    beds = IntegerField('Ágyak száma', validators=[DataRequired()])
    kitchen = BooleanField('Konyha')
    price = IntegerField('Ár egy éjszakára', validators=[DataRequired()])
    status = SelectField('Állapot: ', choices=[(1, 'Elérhető'), (2, 'Foglalt'), (3, 'Karbantartás alatt')])
    submit_roomadd = SubmitField('Hozzáadás')
    submit_roomupdate = SubmitField('Módosítás')
    submit_roomdelete = SubmitField('Törlés')
