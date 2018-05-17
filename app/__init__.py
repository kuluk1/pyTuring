# Import flask and template operators
from flask import Flask, render_template

# Import database modules
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import for flask_login
from flask_login import LoginManager

# Bootstrap
from flask_bootstrap import Bootstrap



db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
bootstrap = Bootstrap()

def create_app():
    # Define the WSGI application object
    app = Flask(__name__)

    # Configurations
    app.config.from_object('config')

    # init the database object which is imported
    # by modules and controllers
    db.init_app(app=app)
    migrate = Migrate(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    # Import a module / component using its blueprint handler variable (mod_auth)
    from app.mod_auth.controllers import mod_auth as auth_module
    from app.mod_main.controllers import mod_main as main_module

    # Register blueprint(s)
    app.register_blueprint(auth_module)
    app.register_blueprint(main_module)
    # app.register_blueprint(xyz_module)
    # ..
    return app