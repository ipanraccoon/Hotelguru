from hmac import new
import json
from sre_constants import SUCCESS
from urllib import response
from Hotelguru.blueprints.Hotel import bp
from Hotelguru.blueprints.Hotel.schemas import HotelResponseSchema, HotelRequestSchema, HotelReviewRequestSchema, HotelReviewResponseSchema
from Hotelguru.blueprints.Hotel.service import HotelService
from apiflask.fields import String, Integer
from apiflask import HTTPError
from Hotelguru.extensions import auth
from Hotelguru.blueprints import role_required


@bp.get('/listhotels/')
@bp.output(HotelResponseSchema(many=True))
def hotel_list_all():
    success, response = HotelService.hotel_list_all()
    if not success:
        raise HTTPError(400, message=response)
    return response

@bp.get('/listhotels/<city>')
@bp.output(HotelResponseSchema(many=True))
def hotel_list_city(city):
    success, response = HotelService.hotel_list_city(city)
    
    if success:
        return response, 200
    return {"message": response}, 400

@bp.post('/addhotel/')
@bp.input(HotelRequestSchema)
@bp.output(HotelResponseSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def hotel_add(json_data):
    success, response = HotelService.hotel_add(json_data)

    if not success:
       return {"message": response}, 400
    return response

@bp.put('/deletehotel/<int:hid>')
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def hotel_delete(hid):
    success, response = HotelService.hotel_delete(hid)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.post('/review/add')
@bp.input(HotelReviewRequestSchema, location="json")
@bp.output(HotelReviewResponseSchema)
def add_review(json_data):

    success, response = (HotelService.add_review(json_data))

    if success:
        return response, 200

    return {"message": response}, 400
