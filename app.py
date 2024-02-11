from flask import Flask,jsonify
from flask_smorest import Api
from db import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

import os
from urllib.parse import quote_plus

from alembic import command
from alembic.config import Config
from sqlalchemy.orm.exc import NoResultFound

from blocklist import BLOKLIST
import models

from resources.lawyer import blp as LawyerBlueprint
from resources.review import blp as ReviewBlueprint
from resources.user import blp as UserBlueprint
from resources.appointement import blp as AppointementBlueprint

def create_app(db_url = None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    #for documentation / for flask smorest
    app.config["API_TITLE"] = "lawyers REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL" , "mysql+pymysql://root:6@5@7#YOUNES643@localhost/dzmouhami")
    

    password = quote_plus('6@5@7#YOUNES643')
    db_url = f"mysql+pymysql://root:{password}@localhost/dzmouhami"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app , db)
    app.config["JWT_SECRET_KEY"] = '255517910574667075310041888667322598649'
    jwt = JWTManager(app)

    with app.app_context():
        try:
            result = db.session.query(models.LawyerModel).first()
        except NoResultFound:
            alembic_cfg = Config("./migrations/alembic.ini")
            command.upgrade(alembic_cfg, "head")
        else:
            print("Database is not empty.")

    #jwt configuration
    @jwt.token_in_blocklist_loader
    def chek_BlockList_tokens(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOKLIST    #jti is a key in the payload define each jwt token 
    
    @jwt.revoked_token_loader  #when the token is revoked that is the error message 
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {"description": "the token has been revoked" , "error": "token_revoked"}
            ),401
        )
    
    #some configuration for jwt to handle authentication and error
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header , jwt_payload):
        return (
            jsonify(
                {"message" : "the token has expired" , "error" : "invalid token"}
            ), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message" : "Signature verification failed" , "error" : "invalid token"}
            ), 401
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {"description" : "token does not contain an access token" , "error" : "authorization required"}
            ),401
        )
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description" : "token is not fresh",
                    "error" : "fresh_token required"
                }
            ), 401
        )
    @jwt.additional_claims_loader
    def additional_claims_to_jwt(identity): #identity is what you have used to generate a jwt token in login 
        if identity == 1 :
            return {"is_admin" : True}
        else : # the claims is saved in the jwt when it created not when it's used
            return {"is_admin" : False}

    api.register_blueprint(LawyerBlueprint)
    api.register_blueprint(ReviewBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AppointementBlueprint)
    return app
