from db import db

class UserModel(db.Model):  
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(40), nullable = False)

    reviews = db.relationship("ReviewModel",  back_populates="user", lazy="dynamic")
    appointments = db.relationship("AppointementModel",  back_populates="user", lazy="dynamic")