from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rabadiom.recommender.utils import unique_specialities

class Recommend(FlaskForm):
    speciality = SelectField('Speciality', choices=unique_specialities)
    filter = RadioField('Filter By', choices=[('rating', 'Rating'),('rate', 'Rate'),('distance', 'Distance')], default='rating')
    #a_or_d = RadioField('Ascending or Descending', choices=[('asc', 'Ascending'),('desc', 'Descending')], default='asc')
    address = StringField('Address')
    submit = SubmitField('Submit')

    def address_not_valid(self):
    	raise ValidationError("Address needs to be filled")
  