from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import backref

#initialize DB and Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

# table Model Class
class Bot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(20))
    menu = db.Column(db.String(80))

    def __init__(self, name, phone, menu):
        self.name=name
        self.phone=phone
        self.menu=menu


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    address = db.Column(db.String(200))
    telephone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(80))
    latitude = db.Column(db.String(80))
    longitude = db.Column(db.String(80))

    def __init__(self, name, address, telephone, mobile, email, latitude, longitude):
        self.name=name
        self.address=address
        self.telephone=telephone
        self.mobile=mobile
        self.email=email
        self.latitude=latitude
        self.longitude=longitude


#Bot Schema
class BotSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'phone', 'menu')

#Bot schema
bot_schema = BotSchema()
bots_schema = BotSchema(many=True)

#Branch Schema
class BranchSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'telephone', 'mobile', 'email', 'latitude', 'longitude')

#initilize schema
branch_schema = BranchSchema()
branches_schema = BranchSchema(many=True)