# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

from flask_login import login_user, logout_user, current_user

mod_main = Blueprint('main', __name__)

@mod_main.route('/')
@mod_main.route('/index')
def index():
    return render_template('index.html')