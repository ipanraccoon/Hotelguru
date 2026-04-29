import json
from sre_constants import SUCCESS
from Hotelguru.blueprints.user import bp
from urllib import response
from Hotelguru.blueprints.user.schemas import UserSchema, RoleSchema, LoginSchema, RegisterSchema, UserUpdateSchema
from Hotelguru.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Integer

@bp.route('/')
def index():
    return 'This is The User Blueprint'

@bp.post('/login')
@bp.doc(responses={400: {"description": "Invalid login"}})
@bp.input(LoginSchema, location="json")
@bp.output(UserSchema, status_code=200)
def user_login(json_data):
    SUCCESS, response = UserService.user_login(json_data)
    if SUCCESS:
        return response, 200
    raise HTTPError(400, message=response)

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
def get_all_roles():
    success, response = UserService.get_all_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/roles/<int:userid>')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
def get_user_roles(userid):
    success, response = UserService.get_user_roles(userid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/<int:userid>')
@bp.doc(tags=["user"])
@bp.output(UserSchema)
def get_user(userid):
    success, response = UserService.get_user(userid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.put('/<int:userid>')
@bp.doc(tags=["user"])
@bp.input(UserUpdateSchema, location="json")
@bp.output(UserSchema)
def update_user(userid, json_data):
    success, response = UserService.update_user(userid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)