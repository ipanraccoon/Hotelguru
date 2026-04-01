from flask import jsonify
from Hotelguru.blueprints.user import bp
from Hotelguru.blueprints.user.schemas import UserSchema, RoleSchema, LoginSchema
from Hotelguru.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer, List

@bp.route('/')
def index():
    return 'This is The User Blueprint'

@bp.post('/login')
@bp.doc(tags=["user"])
@bp.input(LoginSchema, location="json")
@bp.output(UserSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
