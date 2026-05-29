from flask import render_template, request, flash, redirect, session
from Hotelguru.blueprints.main import bp
import requests
from Hotelguru.Forms.loginForm import LoginForm
from Hotelguru.Forms.newRoom import NewRoom
from Hotelguru.Forms.updateRoom import UpdateRoom
from Hotelguru.Forms.deleteRoom import DeleteRoom
from Hotelguru.Forms.registerForm import RegisterForm
from Hotelguru.Forms.updateUser import UpdateForm




def get_user_from_session():
    user = session.get('user')
    if not user:
        return None
    if(requests.get(request.host_url + "getuser",headers={'Authorization': f"Bearer {user['token']}"}).status_code == 200):
        return user
    else:
        session.pop('user', None)
        return None

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def home():
    api_url = request.host_url + "listhotels"
    response = requests.get(api_url)
    hotels = response.json()

    loginform=LoginForm()
    if loginform.validate_on_submit() and loginform.submit_login.data:
        flash("Login requested for user {}".format(loginform.email.data))
        response= requests.post(request.host_url + "login", json={"email": loginform.email.data,"password": loginform.password.data})
        if response.status_code == 200:
            flash("Login successful")
            session['user'] = response.json()
        else:
            flash("Login failed")
        return redirect("/")

    user = get_user_from_session()
    return render_template('main.html', hotels=hotels, login=loginform, user=user)

@bp.route('/reg', methods=['GET', 'POST'])
def register():
    registerform=RegisterForm()
    if registerform.validate_on_submit() and registerform.submit_register.data:
        flash("Register requested for user {}".format(registerform.email.data))
        response= requests.post(request.host_url + "register", json={
            "name": registerform.name.data,
            "phone": registerform.phone.data,
            "email": registerform.email.data,
            "password": registerform.password.data
        })
        if response.status_code == 200:
            flash("Register successful")
        else:
            flash("Register failed")
        return redirect("/")
    return render_template('register.html', register=registerform)

@bp.route('/account', methods=['GET', 'POST'])
def account():
    user = get_user_from_session()
    userdata = requests.get(request.host_url + "getuser",headers={'Authorization': f"Bearer {user['token']}"}).json()
    updateform = UpdateForm()
    if updateform.validate_on_submit() and updateform.submit.data:
        response = requests.put(request.host_url + "updateuser", json={
            "name": updateform.name.data,
            "phone": updateform.phone.data,
            "email": updateform.email.data
        }, headers={'Authorization': f"Bearer {user['token']}"})
        if response.status_code == 200:
            flash("Update successful")
        else:
            flash("Update failed")
        return redirect("/account")
    return render_template('account.html', user=userdata, updateuser=updateform)

@bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect("/")

@bp.route('/rooms/<hid>', methods=['GET', 'POST', 'PUT'])
def rooms(hid):
    api_url = request.host_url + "listrooms/" + hid
    response = requests.get(api_url)
    rooms = response.json()
    
    user = get_user_from_session()
    headers = {}
    if user and 'token' in user:
        headers['Authorization'] = f"Bearer {user['token']}"
    roles = requests.get(request.host_url + "userroles", headers=headers).json()


    newroomform = NewRoom()
    if newroomform.validate_on_submit() and newroomform.submit_add.data:
        response = requests.post(request.host_url + "addhotelroom", json={
            "number": newroomform.number.data,
            "beds": newroomform.beds.data,
            "kitchen": newroomform.kitchen.data,
            "price": newroomform.price.data,
            "status_id": 1,
            "hotel_id": hid
        }, headers=headers)
        if response.status_code == 200:
            flash("Room added successfully")
        else:
            flash("Room add failed")
        return redirect(f"/rooms/{hid}")

    updateroomform=UpdateRoom()
    if updateroomform.validate_on_submit() and updateroomform.submit_update.data:
        response = requests.put(request.host_url + "updateroom/" + str(updateroomform.roomid.data), json={
            "number": updateroomform.number.data,
            "beds": updateroomform.beds.data,
            "kitchen": updateroomform.kitchen.data,
            "price": updateroomform.price.data,
            "status_id": 1,
            "hotel_id": hid
        }, headers=headers)
        if response.status_code == 200:
            flash("Room updated successfully")
        else:
            flash("Room update failed")
        return redirect(f"/rooms/{hid}")

    deleteroomform=DeleteRoom()
    if deleteroomform.validate_on_submit() and deleteroomform.submit_delete.data:
        response = requests.put(request.host_url + "deleteroom/" + str(deleteroomform.roomid.data), headers=headers)
        if response.status_code == 200:
            flash("Room deleted successfully")
        else:
            flash("Room delete failed")
        return redirect(f"/rooms/{hid}")


    return render_template('rooms.html', rooms=rooms, user=user, roles=roles, hid=hid, newroom=newroomform, updateroom=updateroomform, deleteroom=deleteroomform)
