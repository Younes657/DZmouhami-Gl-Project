from db import db

class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80) , nullable=False)
    description =db.Column(db.Text, nullable =False )
    is_recommended = db.Column(db.Boolean, default=False, nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey("lawyers.id"), nullable=False)
    lawyer = db.relationship("LawyerModel",  back_populates="reviews")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel",  back_populates="reviews")
    #lawyer = db.relationship("LawyerModel", backref=db.backref("reviews", lazy="dynamic"))

    #we should add the user id when we create it