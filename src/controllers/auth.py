from main import db
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models.User import User
from forms.forms import RegistrationForm
from forms.forms import InfoForm
from flask import jsonify
from flask_login import current_user

from flask_wtf import FlaskForm

from wtforms.fields.html5 import DateField
from wtforms import validators, SubmitField
auth = Blueprint('auth', __name__)


# Signup Route

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        form = RegistrationForm()
        if form.validate():
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')
            new_user = User(email=email, name=name,password=generate_password_hash(password, method='sha256'),valid=False, membership="None", valid_till="None", is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            flash('Please Log in below')
            return redirect(url_for('main.profile'))
    except Exception:
        flash('Email already registered')
        render_template('signup.html', form=form, error=form.errors)

    return render_template('signup.html', form=form, error=form.errors)

@auth.route('/login')
def login():
    return render_template('login.html')



# Login Route

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))



# Logout Route

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



# User Password Change Route

@auth.route('/profile', methods=["POST"])
@login_required
def user_password_change():
    user_id = current_user._get_current_object()
    password = request.form.get('password')
    if len(password) < 6:
        flash('Password not valid')
        return redirect(url_for('main.profile'))
    else:
        user_id.password = generate_password_hash(password, method='sha256')
        db.session.commit()
        flash('Password changed')

    return redirect(url_for('main.profile'))



# @auth.route('/send-mail/')
# def send_mail():
#     from flask.ext.sendmail import Message
#     msg = Message("Hello",
#                   sender="murrumbeenatennis@gmail.com",
#                   recipients=["murrumbeenatennis@gmail.com"])
#     msg.body = "testing"
#     mail.send(msg)
#     return print(msg)
