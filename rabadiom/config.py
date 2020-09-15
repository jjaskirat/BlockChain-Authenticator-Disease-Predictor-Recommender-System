import os


class Config:
    SECRET_KEY = '5491628bb0b13c0c676de280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "rabadiom@gmail.com"
    MAIL_PASSWORD = "Jjaskirat+1"
