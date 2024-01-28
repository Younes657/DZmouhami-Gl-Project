from db import db


class LawyerModel(db.Model):
    __tablename__ = "lawyers"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True , nullable=False)
    address =db.Column(db.String(200), unique=False ,nullable =False )
    #wilaya = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=True)
    phoneNumber = db.Column(db.String(50), nullable=True)
    Categories = db.Column(db.Text, nullable=False)
    password = db.Column(db.String(260), nullable=True)
    rating = db.Column(db.Integer, nullable=False , default=0)
    reviews = db.relationship("ReviewModel",  back_populates="lawyer", lazy="dynamic")
    lawyer_scheduler = db.relationship("LawyerSchedule", back_populates = "lawyer", lazy="dynamic")
