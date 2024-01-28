from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from models import ReviewModel, LawyerModel
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import get_jwt_identity

from schemas import ReviewSchema
blp = Blueprint("reviews" , __name__, description="Opearations on reviews")

@blp.route("/reviews/<int:lawyer_id>")
class Reviews_Lowyer(MethodView):
    @blp.response(200 , ReviewSchema(many=True))
    def get(self , lawyer_id):
        lawyer = LawyerModel.query.get_or_404(lawyer_id)
        reviews = lawyer.reviews
        return reviews
    
@blp.route("/lawyer/<int:lawy_id>/review")
class Lawyer_review(MethodView):
    @blp.arguments(ReviewSchema)
    @blp.response(201 , ReviewSchema)
    def post(self , review_data , lawy_id):
        review = ReviewModel(**review_data , lawyer_id = lawy_id,  user_id = get_jwt_identity())
        try:
            db.session.add(review)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message= SQLAlchemyError._message)
        return review 
    
@blp.route("/user/reviews")
class User_reviews(MethodView):
    @blp.response(200 , ReviewSchema(many=True))
    def get(self):
        pass