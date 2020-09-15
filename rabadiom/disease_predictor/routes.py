from flask import render_template, Blueprint, flash, request
from rabadiom.disease_predictor.forms import SymptomForm, SymptomFinalForm
from flask_login import login_user, current_user, logout_user, login_required
from rabadiom import login_manager
from rabadiom.disease_predictor.utils import predict_disease, predict_using_ml
from wtforms import StringField
from wtforms.validators import DataRequired
from functools import wraps
import math


def login_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            if (current_user.role != role):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


predictor = Blueprint('predictor', __name__)

@predictor.route("/Disease Predictor", methods=['GET', 'POST'])
@login_required("User")
def disease_predictor():
	form = SymptomForm()
	if form.validate_on_submit():
		if form.symptom1.data == "Select":
			return render_template('show_diseases.html', title='Disease Predictor Result')
		symptoms = [form.symptom1.data, form.symptom2.data, form.symptom3.data, form.symptom4.data, form.symptom5.data, form.symptom6.data]
		diseases = predict_using_ml(symptoms)
		#diseases = ',\r\r\n'.join(["disease :" + d[0] + " \nscore :" + str(math.ceil(d[1])) for d in diseases])
		#flash(diseases,"success")
		return render_template('show_diseases.html', title='Disease Predictor Result', diseases=diseases)
	elif request.method == "GET":
		form.symptom1.data = "None"
		form.symptom2.data = "None"
		form.symptom3.data = "None"
		form.symptom4.data = "None"
		form.symptom5.data = "None"
		form.symptom6.data = "None"
	return render_template('disease_predictor.html', title='Disease Predictor', form=form)
