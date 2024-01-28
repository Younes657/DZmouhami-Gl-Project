from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from flask_jwt_extended import get_jwt_identity

from db import db
import models 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from schemas import LawyerScheduleSchema
blp = Blueprint("appointement" , __name__, description="Opearations on appointement")

@blp.route("/appointement/<int:lawy_id>")
class Appointement_Lawyer(MethodView):
    @blp.response(200 ,LawyerScheduleSchema(many = True) )
    def get(selft, lawy_id):
        try:
            lawyer = models.LawyerModel.query.get_or_404(lawy_id)
            return lawyer.lawyer_schedule 
            
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    def post(self , lawy_id):
        data = request.get_json()
        try:
            day = models.DayModel.query.filter(models.DayModel.name == data["day"]).first()
            time = models.TimeModel.query.filter(models.TimeModel.name == data["time"]).first() 
            schedule = models.LawyerSchedule.query.filter(models.LawyerSchedule.day_id == day.id 
                                                        & models.LawyerSchedule.time_id== time.id 
                                                        & models.LawyerSchedule.lawyer_id == lawy_id ).first()
            Appointement = models.AppointementModel(
                user_id = get_jwt_identity(),
                schedule_id = schedule.id
            )
            db.session.add(Appointement)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return Appointement , 201
    
@blp.route("/Appointement")
class Appointement_user(MethodView):
    def get(self):
        try:
            appointements = models.AppointementModel.query.filter(models.AppointementModel.user_id == get_jwt_identity())
            return {"Appointement" : appointements} , 200
        except SQLAlchemyError as e:
            abort(500, message=str(e))