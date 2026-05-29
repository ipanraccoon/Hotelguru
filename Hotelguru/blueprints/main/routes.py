from flask import render_template, request, flash, redirect, session
from Hotelguru.blueprints.main import bp
import requests
from Hotelguru.Forms.loginForm import LoginForm
from Hotelguru.Forms.newRoom import NewRoom
from Hotelguru.Forms.updateRoom import UpdateRoom
from Hotelguru.Forms.deleteRoom import DeleteRoom



@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def home():
    api_url = request.host_url + "listhotels/"
    response = requests.get(api_url)
    hotels = response.json()


    loginform=LoginForm()
    if loginform.validate_on_submit():
        flash("Login requested for user {}".format(loginform.email.data))
        response= requests.post(request.host_url + "login", json={"email": loginform.email.data,"password": loginform.password.data})
        if response.status_code == 200:
            flash("Login successful")
            session['user'] = response.json()
        else:
            flash("Login failed")
        return redirect("/")

    user = session.get('user')
    return render_template('main.html', hotels=hotels, login=loginform, user=user)

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
    
    user = session.get('user')
    headers = {}
    if user and 'token' in user:
        headers['Authorization'] = f"Bearer {user['token']}"
    
    roles = requests.get(request.host_url + "userroles", headers=headers).json()
    print(roles)

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
