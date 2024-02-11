from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from models import UserModel
from sqlalchemy.exc import SQLAlchemyError

from passlib.hash import pbkdf2_sha256 #a hashing algorithm
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt_identity , jwt_required,get_jwt
from blocklist import BLOKLIST

from schemas import UserSchema
blp = Blueprint("users" , __name__, description="Opearations on users")

@blp.route("/register")
class UserRegistration(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message= "user already exist!!") #409 conflict
        emailUser = user_data["email"] if user_data["email"]  else ""
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"]),
            email = emailUser,
            role = "user"
        )
        db.session.add(user)
        db.session.commit()
        return user

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        # raise NotImplementedError("not implemented yet")
        db.session.delete(user)
        db.session.commit()
        return {"message" : "user deleted."}, 200 #default

@blp.route("/users")
class Users(MethodView):
    @blp.response(200 , UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user is not None and pbkdf2_sha256.verify(user_data["password"] , user.password):
            access_token = create_access_token(identity=user.id , fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token , "refresh_token": refresh_token}
        
        abort(401, message="Invalid Credentials")



@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required() #optional = True if you want to log out the user and false otherwise
    def post(self):
        jti = get_jwt()["jti"] #get_jwt().get("jti") 
        BLOKLIST.add(jti)
        return {"message": "Successfully logged out"}


@blp.route("/refresh")
class TokenRefreshView(MethodView):
    @jwt_required()
    def post(self):
        #none if there is no user defined
        current_user = get_jwt_identity() #get_jwt().get("sub")
        new_token  = create_access_token(identity=current_user , fresh=False) #get
        return {'new_access_token': new_token}
