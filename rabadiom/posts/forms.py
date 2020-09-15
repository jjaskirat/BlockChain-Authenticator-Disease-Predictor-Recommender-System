from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList
from wtforms.validators import DataRequired, ValidationError
from rabadiom.models import User



class PostForm(FlaskForm):

    userid = StringField('User ID', validators=[DataRequired()])
    diseases = FieldList(StringField('Probable Disease'), min_entries=3, max_entries=3)
    test_or_med = FieldList(StringField('Suggested Medicine or Test'), min_entries=7, max_entries=7)
    causes = FieldList(StringField('Why?'), min_entries=7, max_entries=7)

    submit = SubmitField('Post')


    def validate_userid(self, userid):
        user = User.query.filter_by(username=userid.data).first()
        if not user:
            raise ValidationError('No Such User Exists')
        elif user.role == "Doctor":
        	raise ValidationError('The ID Provided is the ID of a Doctor')