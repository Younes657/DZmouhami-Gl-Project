from db import db
from sqlalchemy.dialects.mysql import TIME

class DayModel(db.Model):
    __tablename__ = "Days"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True , nullable=False)
    times = db.relationship("TimeModel" , back_populates="days" , secondary="Lawyer_Schedule")
    
class TimeModel(db.Model):
    __tablename__ = "Times"

    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(TIME(), nullable=False)
    end_time = db.Column(TIME(), nullable=False)
    days = db.relationship("DayModel" , back_populates="times" , secondary="Lawyer_Schedule")

    
    # __table_args__ = (
    #     PrimaryKeyConstraint('col1', 'col2'),
    # )