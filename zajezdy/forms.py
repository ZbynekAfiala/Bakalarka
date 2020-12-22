from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ZajezdForm(FlaskForm):
    
    title = StringField('Název:',validators=[DataRequired()])
    price = IntegerField('Cena:',validators=[DataRequired()])
    destination = StringField('Destinace:', validators=[DataRequired()])
    date_of_activity = StringField('Datum konání:',validators=[DataRequired()])
    submit = SubmitField('Nabídnout !')
