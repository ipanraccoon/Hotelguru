from flask import jsonify
from Hotelguru.blueprints.user import bp
from Hotelguru.blueprints.user.schemas import UserSchema, RoleSchema, LoginSchema, RegisterSchema
from Hotelguru.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Email, Nested, Integer

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

@bp.post('/register')
@bp.doc(tags=["user"])
@bp.input(RegisterSchema, location="json")
@bp.output(UserSchema)
def user_register(json_data):
    success, response = UserService.user_register(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/roles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
def get_roles():
    success, response = UserService.get_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)