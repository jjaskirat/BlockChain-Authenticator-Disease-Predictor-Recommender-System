from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from rabadiom.config import Config





db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    


    from rabadiom.users.routes import users
    from rabadiom.posts.routes import posts
    from rabadiom.main.routes import main
    from rabadiom.disease_predictor.routes import predictor
    from rabadiom.errors.handlers import errors
    from rabadiom.doctor.routes import doctor
    from rabadiom.doc_main.routes import doc_main
    from rabadiom.blockchain.routes import bchain
    from rabadiom.recommender.routes import recommend

    app.register_blueprint(recommend)
    app.register_blueprint(doc_main)
    app.register_blueprint(doctor)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(predictor)
    app.register_blueprint(errors)
    app.register_blueprint(bchain)


    
    return app
