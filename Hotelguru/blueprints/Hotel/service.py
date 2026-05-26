from datetime import datetime
from numbers import Number
import traceback
from turtle import st
from flask import request_tearing_down
from Hotelguru.extensions import db
from Hotelguru.blueprints.Hotel.schemas import HotelResponseSchema, HotelRequestSchema, HotelReviewRequestSchema, HotelReviewResponseSchema
from Hotelguru.models import Reservation, ReservationRoom, Room
from Hotelguru.models.Hotel import Hotel
from Hotelguru.models.User import User
from Hotelguru.models.HotelReview import HotelReview
from sqlalchemy import False_, Select, select, and_, func

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

    @staticmethod
    def add_review(data):
        try:

            hotel = db.session.get(Hotel, data["hotel_id"])

            if not hotel:
                return False, "Hotel not found"

            user = db.session.get(User, data["user_id"])

            if not user:
                return False, "User not found"

            reservation_exists = db.session.execute(
                select(Reservation.id)
                .join(ReservationRoom, Reservation.id == ReservationRoom.reservation_id)
                .join(Room, ReservationRoom.room_id == Room.id)
                .where(Reservation.user_id == data["user_id"])
                .where(Room.hotel_id == data["hotel_id"])
                ).first()

            if not reservation_exists:
                return False, "Reservation not found"

            existing_review = db.session.execute(
                select(HotelReview)
                .where(HotelReview.user_id == data["user_id"])
                .where(HotelReview.hotel_id == data["hotel_id"])
            ).scalar_one_or_none()

            if existing_review:
                return False, "Already reviewed"

            review = HotelReview()

            review.user_id = data["user_id"]
            review.hotel_id = data["hotel_id"]
            review.rating = data["rating"]
            review.comment = data.get("comment")
            review.created_at = datetime.now()

            db.session.add(review)
            db.session.flush()

            avg_rating = db.session.execute(
                select(func.avg(HotelReview.rating))
                .where(HotelReview.hotel_id == data["hotel_id"])
                ).scalar()

            hotel.rating = round(avg_rating, 1)

            db.session.commit()

            return True, (HotelReviewResponseSchema().dump(review))



        except Exception as ex:
            db.session.rollback()
            return False, str(ex)


