from main import db
from flask import Blueprint
from command_functions import time_date_slots


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from datetime import date
    from datetime import timedelta
    import datetime
    from datetime import datetime
    from models.User import User   
    from models.Bookings import Bookings 

    import json                 
    from werkzeug.security import generate_password_hash                                     
    from faker import Faker                                    

    faker = Faker()
    users = []
    bookings = []

    # Create users and  add to db - first user is admin

    for i in range(15):                                               
        user = User() 
        password = "123456"  
        password = generate_password_hash(password, method='sha256')                                                             
        if i == 0:
            user.is_admin = True
        else:
            user.is_admin = False

        user.email = f"test{i+1}@test.com" 
        user.name = faker.name()

        user.membership = "None"
        user.valid = False
        user.valid_till = "None"
                            
        user.password = password
        db.session.add(user)                                                
        users.append(user)                                                     

    db.session.commit()

    # Add time slots for each date into the DB
    # timeslots gathered from time_date_slot()

    date_times = time_date_slots()
    

    for k, v in date_times.items():
        for b, c in v.items():  
            for d in c:
                booking = Bookings()
                booking.date = k
                booking.court = b
                booking.time_slot = d

                db.session.add(booking)

    db.session.commit()  




