from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from rabadiom import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from rabadiom.models import Post, User, Ehr, Keys
from rabadiom.doctor.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from rabadiom.users.utils import save_picture, send_reset_email
from functools import wraps
from rabadiom.blockchain import blockchain
from rabadiom.blockchain.utils import Doctor, GetPublicKey, GetPrivateKey

doctor = Blueprint('doctor', __name__)

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


@doctor.route("/Doctor/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('doc_main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, username=form.username.data, email=form.email.data, password=hashed_password,role="Doctor")
        doctor = Doctor(name = user.name)
        private_key = GetPrivateKey(doctor.private_key)
        public_key = GetPublicKey(doctor.public_key)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        keys = Keys(user_id = user.id, public_key = public_key, private_key = private_key)
        db.session.add(keys)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('doctor.login'))
    return render_template('doc_register.html', title='Doctor Register', form=form)


@doctor.route("/Doctor/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role != "User":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been succesfully logged in!!', 'success')
            #flash(str(current_user))
            return redirect(next_page) if next_page else redirect(url_for('doc_main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('doc_login.html', title='Doctor Login', form=form)


@doctor.route("/Doctor/logout")
def logout():
    logout_user()
    return redirect(url_for('doc_main.home'))


@doctor.route("/Doctor/account", methods=['GET', 'POST'])
@login_required("Doctor")
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
        return redirect(url_for('doctor.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('doc_account.html', title='Account',
                           image_file=image_file, form=form)

@login_required("Doctor")
@doctor.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@doctor.route("/Doctor/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('doc_main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Dcotor.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('doctor.login'))
    return render_template('doc_reset_request.html', title='Reset Password', form=form)


@doctor.route("/Doctor/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('doc_main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('doctor.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('doctor.login'))
    return render_template('doc_reset_token.html', title='Reset Password', form=form)
