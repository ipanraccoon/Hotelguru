import json
import traceback
from sre_constants import SUCCESS
from urllib import response
from Hotelguru.blueprints.room import bp
from Hotelguru.blueprints.room.schemas import RoomRequestSchema, RoomResponseSchema, RoomStatusSchema, RoomListSchema
from Hotelguru.blueprints.room.service import RoomService
from apiflask.fields import String, Integer
from apiflask import HTTPError


@bp.post('/addhotelroom/')
@bp.input(RoomRequestSchema)
@bp.output(RoomResponseSchema)
def room_add(json_data):
    succes, response = RoomService.room_add(json_data)

    if not success:
        return {"message": response}, 400
    return response


@bp.get('/listrooms/')
@bp.output(RoomListSchema(many=True))
def room_list_all():
    success, response = RoomService.room_list_all()
    if not success:
        raise HTTPError(400, message=response)
    return response

@bp.get('/listrooms/<int:hid>')
@bp.output(RoomListSchema(many=True))
def room_list_hotel(hid):
    succes, response  = RoomService.room_list_hotel(hid)

    if succes:
        return response, 200
    return {"message": response}, 400


@bp.put('/updateroom/<int:rid>')
@bp.input(RoomRequestSchema, location="json")
@bp.output(RoomResponseSchema)
def room_update(rid, json_data):
    success, response = RoomService.room_update(rid, json_data)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/deleteroom/<int:rid>')
def room_delete(rid):
    success, response = RoomService.room_delete(rid)
    if success:
        return response, 200
    return {"message": response}, 400