from flask import render_template, request, flash, redirect, session, url_for
from Hotelguru.blueprints.main import bp
import requests
from Hotelguru.Forms.loginForm import LoginForm
from Hotelguru.Forms.roomForms import NewRoom, UpdateRoom, DeleteRoom
from Hotelguru.Forms.registerForm import RegisterForm
from Hotelguru.Forms.updateUser import UpdateForm
from Hotelguru.Forms.hotelForms import NewHotel, UpdateHotel, DeleteHotel
from Hotelguru.Forms.searchForm import SearchForm, RoomSearchForm



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
    city_filter = request.args.get('city')
    name_filter = request.args.get('name')
    if name_filter and city_filter:
        hotels = requests.get(request.host_url + "listhotels/" + city_filter).json()
        hotels = [hotel for hotel in hotels if name_filter.lower() in hotel['name'].lower()]
    elif city_filter and not name_filter:
        hotels = requests.get(request.host_url + "listhotels/" + city_filter).json()
    else:
        hotels = requests.get(request.host_url + "listhotels").json()
        if name_filter:
            hotels = [hotel for hotel in hotels if name_filter.lower() in hotel['name'].lower()]


    loginform=LoginForm()
    if loginform.validate_on_submit() and loginform.submit_login.data:
        response = requests.post(request.host_url + "login", json={"email": loginform.email.data, "password": loginform.password.data})
        if response.status_code == 200:
            flash("Login successful")
            session['user'] = response.json()
        else:
            flash("Login failed")
        return redirect("/")
    
    user = get_user_from_session()
    roles = []
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()

    if user:
        headers = {'Authorization': f"Bearer {user['token']}"}
    else:
        headers = {}

    searchform = SearchForm()
    if searchform.validate_on_submit() and searchform.submit_search.data:
        return redirect(url_for('main.home', name=searchform.name.data, city=searchform.city.data))

    newhotelform = NewHotel()
    if newhotelform.validate_on_submit() and newhotelform.submit_add.data:
        response = requests.post(request.host_url + "addhotel", json={
            "name": newhotelform.name.data,
            "city": newhotelform.city.data,
            "address": newhotelform.address.data
        }, headers=headers)
        if response.status_code == 200:
            flash("Hotel added successfully")
        else:
            flash("Hotel add failed")
        return redirect("/")
    
    updatehotelform = UpdateHotel()
    if updatehotelform.validate_on_submit() and updatehotelform.submit_update.data:
        pass

    deletehotelform = DeleteHotel()
    if deletehotelform.validate_on_submit() and deletehotelform.submit_delete.data:
        response = requests.put(request.host_url + "deletehotel/" + str(deletehotelform.hotelid.data), headers=headers)
        if response.status_code == 200:
            flash("Hotel deleted successfully")
        else:
            flash("Hotel delete failed")
        return redirect("/")



    return render_template(
        'main.html', 
        hotels=hotels, login=loginform, user=user,roles=roles, 
        newhotel=newhotelform, updatehotel=updatehotelform, 
        deletehotel=deletehotelform, search=searchform)

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
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date and end_date:
        rooms = requests.get(request.host_url + "avalible?start_date="+start_date+"&end_date="+end_date).json()
        rooms = [room for room in rooms if room['hotel']['id'] == int(hid)]
        if not rooms:
            rooms = requests.get(request.host_url + "listrooms/" + hid).json()
            flash("No rooms available")
    else:
        rooms = requests.get(request.host_url + "listrooms/" + hid).json()
    
    user = get_user_from_session()
    roles = []
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()
        headers = {'Authorization': f"Bearer {user['token']}"}
    else:
        headers = {}
        
    services = requests.get(request.host_url + "services/" + hid).json()

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

    updateroomform = UpdateRoom()
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

    deleteroomform = DeleteRoom()
    if deleteroomform.validate_on_submit() and deleteroomform.submit_delete.data:
        response = requests.put(request.host_url + "deleteroom/" + str(deleteroomform.roomid.data), headers=headers)
        print(response)
        if response.status_code == 200:
            flash("Room deleted successfully")
        else:
            flash("Room delete failed")
        return redirect(f"/rooms/{hid}")

    roomsearchform = RoomSearchForm()
    if roomsearchform.validate_on_submit() and roomsearchform.submit_search.data:
        return redirect(url_for('main.rooms', hid=hid, start_date=roomsearchform.start_date.data, end_date=roomsearchform.end_date.data))


    return render_template(
        'rooms.html', 
        rooms=rooms, user=user, roles=roles, hid=hid, 
        services=services, newroom=newroomform, 
        updateroom=updateroomform, deleteroom=deleteroomform,
        roomsearch=roomsearchform
    )
