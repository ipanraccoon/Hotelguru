import json
import traceback
from sre_constants import SUCCESS
from urllib import response
from Hotelguru.blueprints.room import bp
from Hotelguru.blueprints.room.schemas import RoomRequestSchema, RoomResponseSchema, RoomStatusSchema, RoomListSchema, RoomAvalibleDateSchema, RoomStatusUpdateSchema
from Hotelguru.blueprints.room.service import RoomService
from apiflask.fields import String, Integer
from apiflask import HTTPError
from Hotelguru.extensions import auth
from Hotelguru.blueprints import role_required


@bp.post('/addhotelroom/')
@bp.input(RoomRequestSchema)
@bp.output(RoomResponseSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def room_add(json_data):
    success, response = RoomService.room_add(json_data)

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
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def room_update(rid, json_data):
    success, response = RoomService.room_update(rid, json_data)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/deleteroom/<int:rid>')
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def room_delete(rid):
    success, response = RoomService.room_delete(rid)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/roomstatus/<int:rid>')
@bp.input(RoomStatusUpdateSchema, location="json")
@bp.output(RoomResponseSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def room_update_status(rid, json_data):
    success, response = RoomService.room_update_status(rid, json_data["status_id"])
    if success:
        return response, 200
    return {"message": response}, 400

@bp.get('/avalible')
@bp.input(RoomAvalibleDateSchema, location="query")
@bp.output(RoomListSchema(many=True))
def room_list_avalibe(query_data):
    succes, response = RoomService.room_list_date(query_data["start_date"], query_data["end_date"])

    if succes:
        return response, 200
    return {"message":response}, 400

@bp.get('/available/<city>/<start_date>/<end_date>')
@bp.output(RoomListSchema(many=True))
def room_available(city, start_date, end_date):

    success, response = RoomService.room_list_available(
        city,
        start_date,
        end_date
    )

    if success:
        return response, 200

    return {"message": response}, 400