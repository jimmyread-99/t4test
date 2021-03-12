from main import db


class Bookings(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    date =  db.Column(db.Date)
    court = db.Column(db.String(100))
    time_slot = db.Column(db.String(100))
    booking_type = db.Column(db.String(100))
    name = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id")) 






