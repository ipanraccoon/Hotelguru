from datetime import datetime
from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List, Date, DateTime
from apiflask.validators import Length, OneOf, Email
from Hotelguru.models.Room import Room
from Hotelguru.models.RoomStatus import RoomStatus

class HotelResponseSchema(Schema):

    id = fields.Integer()
    name = fields.String()
    city = fields.String()
    address = fields.String()
    rating = fields.Float()

class HotelRequestSchema(Schema):
    name = fields.String()
    city = fields.String()
    address = fields.String()

class HotelUpdateSchema(Schema):
    name = fields.String()
    city = fields.String()
    address = fields.String()
    rating = fields.Float(required=False, allow_none=True)

class HotelReviewRequestSchema(Schema):

    user_id = Integer(required=True)

    hotel_id = Integer(required=True)

    rating = Integer(required=True)

    comment = String()

class HotelReviewResponseSchema(Schema):

    id = Integer()

    rating = Integer()

    comment = String()

    created_at = DateTime()

    user_id = Integer()

    hotel_id = Integer()