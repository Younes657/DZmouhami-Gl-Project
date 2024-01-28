from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from models import LawyerModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from standard_functions import scrape_lawyers

from schemas import LawyerSchema
blp = Blueprint("lawyers" , __name__, description="Opearations on lawyers")

@blp.route("/lawyer/<int:lawyer_id>")
class lawyer(MethodView):
    @blp.response(200, LawyerSchema)
    def get(self , lawyer_id):
        lawyer = LawyerModel.query.get_or_404(lawyer_id)
        return lawyer
    def delete(self, lawyer_id):
        # jwt = get_jwt()
        # if not jwt.get("is_admin"):
        #     abort(401 , message  = "admin privillage  required for delete")

        lawyer = LawyerModel.query.get_or_404(lawyer_id)
        db.session.delete(lawyer)
        db.session.commit()
        return {"message" : "lawyer deleted successfully."} , 200 #default
    @blp.arguments(LawyerSchema)
    @blp.response(201, LawyerSchema)
    def put(self, lawyer_data, lawyer_id):
        lawyer =  LawyerModel.query.get_or_404(lawyer_id)
        lawyer.name = lawyer_data["name"]
        lawyer.address = lawyer_data["address"]
        lawyer.email = lawyer_data["email"]
        lawyer.phoneNumber = lawyer_data["phoneNumber"]
        lawyer.Categories = lawyer_data["Categories"]
        db.session.add(lawyer)
        db.session.commit()
        return lawyer


@blp.route("/lawyer")
class itemList(MethodView):
    #jwt_required()
    @blp.response(200 , LawyerSchema(many=True))
    def get(self):
        return LawyerModel.query.all()
    #authorisation for creating a new lawyer
    #@jwt_required()
    @blp.arguments(LawyerSchema)
    @blp.response(201 , LawyerSchema)
    def post(self , item_data):
        lawyer = LawyerModel(**item_data)
        try:
            db.session.add(lawyer)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= SQLAlchemyError._message)
        return lawyer 
@blp.route("/lawyer/location")
class SearchLawyerAdd(MethodView):
    @blp.response(200, LawyerSchema(many=True))
    def post(self ):
        searchByAdd = request.get_json()
        search = f"%{searchByAdd["location"]}%"
        return LawyerModel.query.filter(LawyerModel.address.like(search)).all()

@blp.route("/lawyer/category")
class SearchLawyerCat(MethodView):
    @blp.response(200, LawyerSchema(many=True) )
    def post(self ):
        searchByCat = request.get_json()
        search = f"%{searchByCat["category"]}%"
        return LawyerModel.query.filter(or_(LawyerModel.Categories.like(search), LawyerModel.name.like(search))).all()
    
@blp.route("/scrape_store")
class ScrapeStore(MethodView):
    def get(self):
        result = db.session.query(LawyerModel).first()
        if result is None:
            scrape_lawyers()
            return {"message" : "lawyers scrap"}
        else :
            return {"message" :"data exist in the database"}




