import json
from Hotelguru.blueprints.user import bp
from Hotelguru.blueprints import role_required
from urllib import response
from Hotelguru.blueprints.user.schemas import UserSchema, RoleSchema, LoginSchema, RegisterSchema, UserUpdateSchema, AssignRoleSchema
from Hotelguru.blueprints.user.service import UserService
from apiflask import HTTPError
from apiflask.fields import String, Integer
from Hotelguru.extensions import auth


@bp.route('/')
def index():
    return 'This is The User Blueprint'

@bp.post('/login')
@bp.doc(responses={400: {"description": "Invalid login"}})
@bp.input(LoginSchema, location="json")
@bp.output(UserSchema, status_code=200)
def user_login(json_data):
    sucess, response = UserService.user_login(json_data)
    if sucess:
        return response, 200
    return {"message": response}, 400

@bp.post('/register')
@bp.doc(tags=["user"])
@bp.input(RegisterSchema, location="json")
@bp.output(UserSchema)
def user_register(json_data):
    success, response = UserService.user_register(json_data)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.get('/roles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
def get_all_roles():
    success, response = UserService.get_all_roles()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@bp.get('/userroles')
@bp.doc(tags=["user"])
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["Vendég"])
def get_user_roles():
    success, response = UserService.get_user_roles()
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/assignrole/<int:userid>')
@bp.doc(tags=["user"])
@bp.input(AssignRoleSchema, location="json")
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def assign_role(userid, json_data):
    success, response = UserService.assign_role(userid, json_data["role_id"])
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/removerole/<int:userid>')
@bp.doc(tags=["user"])
@bp.input(AssignRoleSchema, location="json")
@bp.output(RoleSchema(many=True))
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def remove_role(userid, json_data):
    success, response = UserService.remove_role(userid, json_data["role_id"])
    if success:
        return response, 200
    return {"message": response}, 400

@bp.get('/<int:userid>')
@bp.doc(tags=["user"])
@bp.output(UserSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def get_user(userid):
    success, response = UserService.get_user(userid)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.get('/getuser')
@bp.doc(tags=["user"])
@bp.output(UserSchema)
@bp.auth_required(auth)
def get_current_user():
    userid=auth.current_user["user_id"]
    success, response = UserService.get_user(userid)
    if success:
        return response, 200
    return {"message": response}, 400

@bp.put('/updateuser')
@bp.doc(tags=["user"])
@bp.input(UserUpdateSchema, location="json")
@bp.output(UserSchema)
@bp.auth_required(auth)
def update_user(json_data):
    success, response = UserService.update_user(json_data)
    if success:
        return response, 200
    return {"message": response}, 400