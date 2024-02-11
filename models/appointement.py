from db import db
from sqlalchemy import PrimaryKeyConstraint

class AppointementModel(db.Model):
    __tablename__ = "Appointements"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("Lawyer_Schedule.id"), nullable=False)
    user = db.relationship("UserModel",  back_populates="appointments")
    schedule = db.relationship("LawyerSchedule",  back_populates="appointments")
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'schedule_id'),
    )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'schedule_id': self.schedule_id,
            'user' : self.user,
            'schedule' : self.schedule
        }