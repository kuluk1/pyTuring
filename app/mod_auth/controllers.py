# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module forms
from app.mod_auth.forms import LoginForm, RegisterForm

# Import module models (i.e. User)
from app.mod_auth.models import User

from flask_login import login_user, logout_user, current_user, login_required

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))


    # If sign in form is submitted
    form = LoginForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):

            flash('Welcome %s' % user.username)
            login_user(user)

            return redirect(url_for('main.index'))

        flash('Wrong email or password', 'error-message')

    return render_template("auth/signin.html", form=form)

@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if u is not None:
            flash('Select a differente username')
            redirect(url_for('auth.register'))
        e = User.query.filter_by(email=form.email.data).first()
        if e is not None:
            flash('Select a different email')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.signin'))

    return render_template("auth/register.html", form=form)

@mod_auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
