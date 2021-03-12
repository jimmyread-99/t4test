from main import db
from flask import Blueprint, render_template, redirect
from flask import url_for, request, flash
from flask_login import login_required, current_user
from flask import Blueprint, request, jsonify, abort, render_template 
from flask_wtf import FlaskForm

from wtforms.fields.html5 import DateField
from wtforms import validators, SubmitField
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange

import json               
from datetime import datetime
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from models.Bookings import Bookings
from models.User import User


main = Blueprint('main', __name__)



# Nav Bar Routes

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/play')
def play():
    return render_template("play.html")


@main.route('/calendar')
def calendar():
    return render_template("calendar.html")


@main.route('/memberships')
def memberships():
    return render_template("memberships.html")


@main.route('/contact')
def contact():
    return render_template("contact.html")


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/date')
def date():
    return render_template('date.html')
    

@main.route('/lessons', methods=["GET"])
@login_required
def get_lessons():

    lessons = Bookings.query.filter((Bookings.booking_type) == "Lesson").all()
    return render_template('lessons.html',lessons=lessons)


@main.route('/profile')
@login_required
def profile():
    user_id = current_user._get_current_object()
    sessions = Bookings.query.filter_by(user_id=user_id.id).order_by(Bookings.date.desc()).all()
    lessons = Bookings.query.filter((Bookings.booking_type) == "Lesson").all()

    return render_template('profile.html', sessions=sessions, lessons=lessons)
















# Admin Routes



@main.route('/users/query', methods=['GET'])
@login_required
def query_users():
    user= current_user._get_current_object()
    try:
        if user.is_admin == True:
            users = User.query.all()
            return render_template('users.html', users=users)
        else:
            return render_template('index.html')
    except (Exception):
        return render_template('index.html')



@main.route('/users/query/<int:user_id>', methods=["GET"])
@login_required
def get_single_users(user_id):
    user= current_user._get_current_object()
    try:
        if user.is_admin == True:
            users = User.query.filter_by(id=user_id).one()
            return render_template('user_edit.html', users=users)
        else:
            return render_template('index.html')
    except (Exception):
        return render_template('index.html')



@main.route('/users/query/<int:user_id>/update', methods=["POST"])
@login_required
def edit_single_users(user_id):   
    user= current_user._get_current_object()
    try:
        if user.is_admin == True:
            update_user = User.query.filter_by(id=user_id).first()
            update_user.email = request.form.get("email")
            update_user.name = request.form.get("name")
            update_user.membership = request.form.get("membership")
            update_user.valid_till = request.form.get("valid_till")
            update_user.valid = request.form.get("valid")

            db.session.commit()
            return render_template('user_edit.html',users=update_user)
        else:
            return render_template('index.html')
    except (Exception):
        return render_template('index.html')
        
# Create Lesson Route
@main.route('/lessons/create/<int:booking_id>', methods=["GET", "POST"])
@login_required
def create_lessons(booking_id):
    user = current_user._get_current_object()
    update_booking = Bookings()
    update_booking = Bookings.query.filter_by(id=booking_id).one()

    try:
        if user.is_admin == True:
            update_booking.user_id = None
            update_booking.booking_type = "Lesson"
            update_booking.name = None
            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)
        else:
            return render_template('session_confirm.html',session=update_booking)
    except:
        return render_template('date.html',session=update_booking)















# Booking Routes


@main.route('/query', methods=['GET'])
def query_date():

    try:
        entry = request.args.get('entry')
        bookings = Bookings.query.filter((Bookings.date) == entry).all()
        return render_template('date.html', bookings=bookings)
    except (Exception):
        return render_template('date.html')




@main.route('/date/book/<int:booking_id>', methods=["GET", "POST"])
@login_required
def booking_entry_create(booking_id):

    try:

        update_booking = Bookings()
        user_id = current_user._get_current_object()
        name = current_user._get_current_object()
        valid = current_user._get_current_object()
        user = user_id.id
        name = name.name
        valid = valid.valid

        update_booking = Bookings.query.filter_by(id=booking_id).one()


        if valid != "True":
            return render_template('date.html',session=update_booking, valid=valid)

        elif update_booking.user_id == None and current_user.is_admin == False and update_booking.booking_type == "Lesson":
            update_booking.user_id = user
            update_booking.name = name

            db.session.commit()
            
            return render_template('session_confirm.html',session=update_booking)

        elif update_booking.user_id == None and current_user.is_admin == False:
            update_booking.booking_type = "Casual"
            update_booking.user_id = user
            update_booking.name = name

            db.session.commit()
            
            return render_template('session_confirm.html',session=update_booking)
        

        elif update_booking.user_id == user:
            return render_template('session_confirm.html',session=update_booking)

        else:
            return render_template('date.html',session=update_booking)
    except:
        return render_template('date.html',session=update_booking)




@main.route('/date/book/<int:booking_id>/cancel', methods=["GET", "POST"])
@login_required
def booking_entry_update(booking_id):

    try:
        update_booking = Bookings()
        update_booking = Bookings.query.filter_by(id=booking_id).one()

        if update_booking.user_id == current_user.id and update_booking.booking_type != "Lesson":

            update_booking.booking_type = None
            update_booking.user_id = None
            update_booking.name = None

            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)

        elif update_booking.user_id == current_user.id and update_booking.booking_type == "Lesson":

            update_booking.user_id = None
            update_booking.name = None

            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)

        elif current_user.is_admin == True and update_booking.booking_type == "Lesson":

            update_booking.user_id = None
            update_booking.name = None

            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)

        elif current_user.is_admin == True and update_booking.booking_type != "Lesson":

            update_booking.user_id = None
            update_booking.booking_type = None
            update_booking.name = None

            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)


        elif current_user.is_admin == True and update_booking.booking_type != "Casual":

            update_booking.user_id = None
            update_booking.booking_type = None
            update_booking.name = None

            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)


        elif update_booking.user_id != current_user.id:
            return render_template('date.html',session=update_booking)
        else:
            return render_template('date.html',session=update_booking)

    except: 
        return render_template('date.html',session=update_booking)



@main.route('/date/book/<int:booking_id>/delete', methods=["GET", "POST"])
@login_required
def booking_entry_delete(booking_id):
    user = current_user._get_current_object()
    update_booking = Bookings()
    update_booking = Bookings.query.filter_by(id=booking_id).one()

    try:
        if user.is_admin == True:
            update_booking.user_id = None
            update_booking.booking_type = None
            update_booking.name = None
            db.session.commit()
            return render_template('session_confirm.html',session=update_booking)
        else:
            return render_template('session_confirm.html',session=update_booking)
    except:
        return render_template('date.html',session=update_booking)










