from marshmallow import Schema , fields

class UserSchema(Schema):  
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True , load_only=True)
    email = fields.Str(required=False)
    role = fields.Str(required=False , dump_only=True)


class PlainLawyerSchema(Schema):
    id = fields.Int(dump_only=True)
    name =fields.Str(required=True)
    address =fields.Str(required=True)
    #wilaya = db.Column(db.String(50), unique=False, nullable=False)
    email = fields.Str(required=False)
    phoneNumber = fields.Str(required=False)
    Categories = fields.Str(required=True)
    password = fields.Str(required=True , load_only=True)
    rating = fields.Int(dump_only=True)


class PlainReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description =fields.Str(required=True)
    is_recommended = fields.Bool(required=True)
    rating = fields.Int(dump_only=True)
    

class LawyerSchema(PlainLawyerSchema):
    reviews = fields.List(fields.Nested(PlainReviewSchema), dump_only = True)
    
class ReviewSchema(PlainReviewSchema):
    lawyer_id = fields.Int(required=True , load_only =True)
    lawyer = fields.Nested(PlainLawyerSchema(), dump_only=True)
    user_id = fields.Int(required=True , load_only =True)
    user = fields.Nested(UserSchema(), dump_only=True)

class LawyerScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    lawyer_id = fields.Int(required=True , load_only =True)
    day_id = fields.Int(required=True , load_only =True)
    time_id = fields.Int(required=True , load_only =True)
    is_disponible = fields.Bool(required= True)
    lawyer = fields.Nested(PlainLawyerSchema(), dump_only=True)