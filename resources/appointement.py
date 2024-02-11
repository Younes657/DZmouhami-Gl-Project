from flask import request , jsonify
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from flask_jwt_extended import get_jwt_identity , jwt_required

from db import db
import models 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_ , and_

from schemas import LawyerScheduleSchema
blp = Blueprint("appointement" , __name__, description="Opearations on appointement")

@blp.route("/appointement/<int:lawy_id>")
class Appointement_Lawyer(MethodView):
    @blp.response(200 ,LawyerScheduleSchema(many = True) )
    def get(selft, lawy_id):
        try:
            lawyer = models.LawyerModel.query.get_or_404(lawy_id)
            return lawyer.lawyer_scheduler 
            
        except SQLAlchemyError as e:
            abort(500, message=str(e))
    

    @jwt_required()
    def post(self , lawy_id):
        data = request.get_json()
        try:
            day = models.DayModel.query.filter(models.DayModel.name == data["day"]).first()
            time = models.TimeModel.query.filter(and_(models.TimeModel.start_time == data["start_time"], models.TimeModel.end_time == data["end_time"])).first() 
            schedule = models.LawyerSchedule.query.filter(and_(models.LawyerSchedule.day_id == day.id 
                                                        ,models.LawyerSchedule.time_id== time.id 
                                                        , models.LawyerSchedule.lawyer_id == lawy_id )).first()
            Appointement = models.AppointementModel(
                user_id = get_jwt_identity(),
                schedule_id = schedule.id
            )
            db.session.add(Appointement)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"appointement " : Appointement} , 201
    
@blp.route("/schedule/<int:lawy_id>")
class ScheduleLawyer(MethodView):
    @blp.response(201,LawyerScheduleSchema())
    def post(selft, lawy_id):
        data = request.get_json()
        try:
            day = models.DayModel.query.filter(models.DayModel.name == data["day"]).first()
            time = models.TimeModel.query.filter(and_(models.TimeModel.start_time == data["start_time"], models.TimeModel.end_time == data["end_time"])).first() 
            schedule = models.LawyerSchedule(lawyer_id = lawy_id , day_id = day.id , time_id = time.id , is_disponible = data["is_disponible"] )
            db.session.add(schedule)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return schedule

# @blp.route("/Appointement")
# class Appointement_user(MethodView):
#     @jwt_required()
#     def get(self):
#         try:
#             appointements = models.AppointementModel.query.filter(models.AppointementModel.user_id == get_jwt_identity()).all()
#             # appointments_data = [appointment.to_dict() for appointment in appointements]
#             return  jsonify(appointements) , 200
#         except SQLAlchemyError as e:
#             abort(500, message=str(e))
