from sre_constants import SUCCESS
from urllib import response
from Hotelguru.blueprints.room import bp
from Hotelguru.blueprints.room.schemas import RoomRequestSchema, RoomResponseSchema, RoomStatusSchema, RoomListSchema
from Hotelguru.blueprints.room.service import RoomService
from apiflask.fields import String, Integer
from apiflask import HTTPError

@bp.route('/')
def index():
    return 'This is The Room Blueprint'

@bp.get('/list/')
@bp.output(RoomListSchema(many=True))
def room_list_all():
    SUCCESS, response = RoomService.room_list_all()
    if SUCCESS:
        return response, 200
    raise HTTPError(message=response, status_code=400)

