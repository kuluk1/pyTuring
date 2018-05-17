# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Define a base model for other database tables to inherit
class Base(UserMixin, db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    username    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(128),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=True)
    status   = db.Column(db.SmallInteger, nullable=True)

    # New instance instantiation procedure
    def __init__(self, username, email):

        self.username     = username
        self.email    = email

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))