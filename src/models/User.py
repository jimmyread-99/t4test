from main import db
from flask_login import UserMixin
from models.Bookings import Bookings
from sqlalchemy.orm import backref     
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    membership = db.Column(db.String(1000))
    valid = db.Column(db.String(1000))
    valid_till = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean())

    bookings = db.relationship("Bookings", backref="user", lazy="dynamic")
