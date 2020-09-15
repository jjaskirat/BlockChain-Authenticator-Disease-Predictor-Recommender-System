from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from rabadiom import db, login_manager
from flask_login import UserMixin, current_user
import os

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_posts = db.relationship('Post', backref='user', lazy=True)
    ehrs = db.relationship('Ehr', backref='user_ehr', lazy=True)
    role = db.Column(db.String(10), nullable=False, default="User")

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Ehr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    diseases1 = db.Column(db.String(20))
    diseases2 = db.Column(db.String(20))
    diseases3 = db.Column(db.String(20))
    test_or_med1 = db.Column(db.String(20))
    causes1 = db.Column(db.String(50))
    test_or_med2 = db.Column(db.String(20))
    causes2 = db.Column(db.String(50))
    test_or_med3 = db.Column(db.String(20))
    causes3 = db.Column(db.String(50))
    test_or_med4 = db.Column(db.String(20))
    causes4 = db.Column(db.String(50))
    test_or_med5 = db.Column(db.String(20))
    causes5 = db.Column(db.String(50))
    test_or_med6 = db.Column(db.String(20))
    causes6 = db.Column(db.String(50))
    test_or_med7 = db.Column(db.String(20))
    causes7 = db.Column(db.String(50))

    def __repr__(self):
        return f"EHR('{self.doctor_id}', '{self.user_id}', '{self.date_posted}')"


class Keys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    public_key = db.Column(db.LargeBinary, nullable=False, unique=True)
    private_key = db.Column(db.LargeBinary, nullable=False, unique=True)

    def __repr__(self):
        return f"User('{self.user_id}', '{self.public_key}', '{self.private_key}')"


class Blockchain(db.Model):
    node = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    ehr = db.Column(db.String(50), nullable=False)
    hash = db.Column(db.String(50), nullable=False)
    prev_hash = db.Column(db.String, nullable=False)
    nonce = db.Column(db.BigInteger, nullable=False)
    tstamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class SignedEhr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diseases1 = db.Column(db.LargeBinary)
    diseases2 = db.Column(db.LargeBinary)
    diseases3 = db.Column(db.LargeBinary)
    test_or_med1 = db.Column(db.LargeBinary)
    causes1 = db.Column(db.LargeBinary)
    test_or_med2 = db.Column(db.LargeBinary)
    causes2 = db.Column(db.LargeBinary)
    test_or_med3 = db.Column(db.LargeBinary)
    causes3 = db.Column(db.LargeBinary)
    test_or_med4 = db.Column(db.LargeBinary)
    causes4 = db.Column(db.LargeBinary)
    test_or_med5 = db.Column(db.LargeBinary)
    causes5 = db.Column(db.LargeBinary)
    test_or_med6 = db.Column(db.LargeBinary)
    causes6 = db.Column(db.LargeBinary)
    test_or_med7 = db.Column(db.LargeBinary)
    causes7 = db.Column(db.LargeBinary)
