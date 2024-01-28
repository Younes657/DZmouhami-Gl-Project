from db import db


class LawyerSchedule(db.Model):
    __tablename__ = "Lawyer_Schedule"

    id = db.Column(db.Integer, primary_key = True)
    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey("Days.id"), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey("Times.id"), nullable=False)
    is_disponible = db.Column(db.Boolean, nullable=False , default=False)
    lawyer = db.relationship("LawyerModel", back_populates = "lawyer_scheduler")
    appointments = db.relationship("AppointementModel", back_populates ="schedule", lazy="dynamic")
