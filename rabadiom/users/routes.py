from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from rabadiom import db, bcrypt, login_manager
from flask_login import current_user, login_required, login_user, logout_user
from rabadiom.models import User, Post, Ehr, Keys
from rabadiom.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from rabadiom.users.utils import save_picture, send_reset_email
from functools import wraps
from rabadiom.blockchain.utils import Patient, Doctor, EHR, Block
from rabadiom.blockchain import blockchain
from rabadiom.blockchain.utils import Patient, GetPublicKey, GetPrivateKey


users = Blueprint('users', __name__)


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

@users.route("/Patient/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        patient = Patient(name = user.name)
        private_key = GetPrivateKey(patient.private_key)
        public_key = GetPublicKey(patient.public_key)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        keys = Keys(user_id = user.id, public_key = public_key, private_key = private_key)
        db.session.add(keys)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Patient Register', form=form)


@users.route("/Patient/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role != "Doctor":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash(str(current_user))
            flash('You have been succesfully logged in!!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Patient Login', form=form)


@users.route("/Patient/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/Patient/account", methods=['GET', 'POST'])
@login_required("User")
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        #flash(current_user.keys)
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@login_required("User")
@users.route("/Patient/My EHRs")
def user_posts():
    try:
        page = request.args.get('page', 1, type=int)
        user = current_user
        posts = Ehr.query.filter_by(user_ehr=user)\
            .paginate(page=page, per_page=10)
        doctors = []
        for post in posts.items:
            doctor = User.query.filter_by(id=post.doctor_id).first()
            doctors.append([post,doctor])
            #pass
        if posts.total == 0:
            raise()
    except:
        return render_template('user_posts.html')
    return render_template('user_posts.html', user=user, doctors=doctors, posts=posts)


@users.route("/Patient/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/Patient/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
