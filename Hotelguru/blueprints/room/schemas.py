from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from Hotelguru.models.Room import Room
from Hotelguru.models.RoomStatus import RoomStatus
from Hotelguru.blueprints.Hotel.schemas import HotelResponseSchema

class RoomRequestSchema(Schema):
    number = fields.Integer()
    beds = fields.Integer()
    kitchen = fields.Boolean()
    price = fields.Integer()
    status_id = fields.Integer()
    hotel_id = fields.Integer()

class RoomStatusSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class RoomResponseSchema(Schema):
    number = fields.Integer()
    beds = fields.Integer()
    kitchen = fields.Boolean()
    price = fields.Integer()
    status = fields.Nested(RoomStatusSchema)
    hotel = fields.Nested(HotelResponseSchema)

class RoomListSchema(Schema):
    id = fields.Integer()
    number = fields.Integer()
    beds = fields.Integer()
    kitchen = fields.Boolean()
    price = fields.Integer()
    status = fields.Nested(RoomStatusSchema)
    hotel = fields.Nested(HotelResponseSchema)