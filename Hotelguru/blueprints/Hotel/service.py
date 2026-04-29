from numbers import Number
import traceback
from flask import request_tearing_down
from Hotelguru.extensions import db
from Hotelguru.blueprints.Hotel.schemas import HotelResponseSchema, HotelRequestSchema
from Hotelguru.models.Hotel import Hotel
from sqlalchemy import Select, select, and_

class HotelService:

    @staticmethod
    def hotel_list_city(city):
        hotels = db.session.execute(select(Hotel).filter(Hotel.city == city)).scalars().all()

        return True, HotelResponseSchema().dump(hotels, many=True)

    @staticmethod
    def hotel_list_all():
        hotels = db.session.execute(select(Hotel)).scalars().all()
        return True, HotelResponseSchema().dump(hotels, many=True)

    @staticmethod
    def hotel_add(request):
        try:
            hotel = Hotel()

            hotel.name = request["name"]
            hotel.city = request["city"]
            hotel.address = request["address"]

            db.session.add(hotel)
            db.session.commit()

            return True, HotelResponseSchema().dump(hotel)
        except Exception as ex:
            db.session.rollback()
            traceback.print_exc()
            return False, "hotel_add() error"

    @staticmethod
    def hotel_update(hid, request):
        try:
            hotel = db.session.get(Hotel, hid)

            if hotel:
                hotel.name = request["name"]
                hotel.address = request["address"]
                hotel.rating = request["rating"]

                db.session.commit()
                return True, HotelResponseSchema().dump(hotel)
        except Exception as ex:
            db.session.rollback()
            return False, "hotel_update() error!"

    @staticmethod
    def hotel_delete(hid):
        try:
            hotel = db.session.get(Hotel, hid)

            if hotel:
                db.session.delete(hotel)
                db.session.commit()

        except Exception as ex:
             db.session.rollback()
             return False, "hotel_delete() error"
        return True, "OK!"



