import json
from sre_constants import SUCCESS
from urllib import response
from Hotelguru.blueprints.Hotel import bp
from Hotelguru.blueprints.Hotel.schemas import HotelResponseSchema, HotelRequestSchema
from Hotelguru.blueprints.Hotel.service import HotelService
from apiflask.fields import String, Integer
from apiflask import HTTPError


@bp.get('/list/')
@bp.output(HotelResponseSchema(many=True))
def hotel_list_all():
    succes, response = HotelService.hotel_list_all()
    if succes:
        return response, 200
    raise HTTPError(status_code=400, message=response)

@bp.get('/list/<city>')
@bp.output(HotelRequestSchema(many=True))
def hotel_list_city(city):
    succes, response = HotelService.hotel_list_city(city)
    
    if succes:
        return response, 200
    raise HTTPError(status_code=400, message=response)
    