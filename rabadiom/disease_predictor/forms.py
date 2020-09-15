from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rabadiom.disease_predictor.utils import unique_symptoms

class SymptomForm(FlaskForm):
    symptom1 = SelectField('Symptom - 1', choices=unique_symptoms)
    symptom2 = SelectField('Symptom - 2', choices=unique_symptoms)
    symptom3 = SelectField('Symptom - 3', choices=unique_symptoms)
    symptom4 = SelectField('Symptom - 4', choices=unique_symptoms)
    symptom5 = SelectField('Symptom - 5', choices=unique_symptoms)
    symptom6 = SelectField('Symptom - 6', choices=unique_symptoms)
    submit = SubmitField('Submit')

    def validate_symptom1(self, idd):
      if idd.data == None:
        raise ValidationError("First Symptom can not be Empty")

class SymptomFinalForm(FlaskForm):
  #symptoms = StringField[]
  #symptom = StringField('Symptom')
  #symptoms.append(symptom)

  symptom = FieldList(StringField('Symptom'), min_entries=6, max_entries=6)
  add_symptom = SubmitField("Add another Symptom")
  submit = SubmitField("Submit")

  