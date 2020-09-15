from flask import render_template, Blueprint, flash, request, redirect, url_for
from rabadiom.recommender.forms import Recommend
from flask_login import login_user, current_user, logout_user
from rabadiom import login_manager
from rabadiom.recommender.utils import sort_by_distance, sort_by_rating, sort_by_rate
import requests, json
from functools import wraps


def login_is_required(role):
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


recommend = Blueprint('recommend', __name__)


#@login_is_required("User")
@recommend.route("/Doctor Recommender", methods=['GET', 'POST'])
def doctor_recommender():
	if(current_user.is_authenticated and current_user.role == "User"):
		pass
	else:
		flash("Please login to access this page", "success")
		return redirect(url_for('users.login'))
	form = Recommend()
	if form.validate_on_submit():
		#flash(form.filter.data,"success")
		doctors = []
		if form.speciality.data == "None":
			flash("Please Enter A Speciality", "Danger")
		if form.address.data == "None":
			flash("Please Enter your Address", "Danger")
			return render_template('doctor_recommender.html', title='Doctor Recommender', form=form)
		
		address = form.address.data
		api_key = 'AIzaSyCukArbjvhnW2JjGBedKNUR5fBfbY2KzWg'
		url = 'https://maps.googleapis.com/maps/api/geocode/json?'
		res_ob = requests.get(url + 'address=' + address + '&key=' + api_key)
		x = res_ob.json()
		try:
			lat = x['results'][0]['geometry']['location']['lat']
			lng = x['results'][0]['geometry']['location']['lng']
		except:
			lat = 0
			lng = 0
		latlang = [lat, lng]
		#flash(str(lat) + str(lng))
		if latlang == [0,0]:
			flash("Enter A Valid Address to Filter by Address", "danger")
			return render_template('doctor_recommender.html', title='Doctor Recommender', form=form)
		if form.filter.data == 'distance':
			doctors = sort_by_distance(latlang[0], latlang[1], form.speciality.data)
		elif form.filter.data == 'rating':
			doctors = sort_by_rating(form.speciality.data)
		else:
			doctors = sort_by_rate(form.speciality.data)
		return render_template('show_map.html', title='Doctor Recommender', doctors=doctors, lat=lat, lng=lng)
	elif request.method == "GET":
		#form.a_or_d = 'asc'
		#form.filter = 'rating'
		#form.speciality = 'None'
		form.address.data = "None"
	return render_template('doctor_recommender.html', title='Doctor Recommender', form=form)



