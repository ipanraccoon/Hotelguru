from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Length, OneOf, Email
from Hotelguru.models.Room import Room
from Hotelguru.models.RoomStatus import RoomStatus

class HotelResponseSchema(Schema):

    id = fields.Integer()
    name = fields.String()
    city = fields.String()
    address = fields.String()
    rating = fields.Float()