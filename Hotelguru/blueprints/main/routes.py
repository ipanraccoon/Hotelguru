from flask import render_template, request, flash, redirect, session, url_for
from Hotelguru.blueprints.main import bp
import requests
from Hotelguru.Forms.loginForm import LoginForm
from Hotelguru.Forms.roomForms import RoomForm
from Hotelguru.Forms.registerForm import RegisterForm
from Hotelguru.Forms.updateUser import UpdateForm
from Hotelguru.Forms.hotelForms import HotelForm
from Hotelguru.Forms.searchForm import SearchForm, RoomSearchForm
from Hotelguru.Forms.serviceForms import ServiceForm
from Hotelguru.Forms.reviewForm import ReviewForm
from Hotelguru.Forms.reserveForm import ReserveForm



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
    headers = {}
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()
        headers = {'Authorization': f"Bearer {user['token']}"}
        

    searchform = SearchForm()
    if searchform.validate_on_submit() and searchform.submit_search.data:
        return redirect(url_for('main.home', name=searchform.name.data, city=searchform.city.data))

    hotelform = HotelForm()
    if hotelform.validate_on_submit():
        if hotelform.submit_add.data:
            response = requests.post(request.host_url + "addhotel", json={
                "name": hotelform.name.data,
                "city": hotelform.city.data,
                "address": hotelform.address.data
            }, headers=headers)
            if response.status_code == 200:
                flash("Hotel added successfully")
            else:
                flash("Hotel add failed")

        elif hotelform.submit_update.data:
            response = requests.put(request.host_url + "updatehotel/" + str(hotelform.hotelid.data), json={
                "name": hotelform.name.data,
                "city": hotelform.city.data,
                "address": hotelform.address.data
            }, headers=headers)
            if response.status_code == 200:
                flash("Hotel updated successfully")
            else:
                flash("Hotel update failed")
        
        elif hotelform.submit_delete.data:
            response = requests.put(request.host_url + "deletehotel/" + str(hotelform.hotelid.data), headers=headers)
            if response.status_code == 200:
                flash("Hotel deleted successfully")
            else:
                flash("Hotel delete failed")
        return redirect("/")



    return render_template(
        'main.html', 
        hotels=hotels, login=loginform, user=user,roles=roles, 
        hotelform=hotelform, search=searchform)

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
    availableRooms = []
    if start_date and end_date:
        rooms = requests.get(request.host_url + "avalible?start_date="+start_date+"&end_date="+end_date).json()
        rooms = [room for room in rooms if room['hotel']['id'] == int(hid)]
        availableRooms = rooms
        if not rooms:
            rooms = requests.get(request.host_url + "listrooms/" + hid).json()
            flash("No rooms available")
    else:
        rooms = requests.get(request.host_url + "listrooms/" + hid).json()
    
    user = get_user_from_session()
    roles = []
    headers = {}
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()
        headers = {'Authorization': f"Bearer {user['token']}"}
     
        
    services = requests.get(request.host_url + "services/" + hid).json()

    roomform = RoomForm()
    if roomform.validate_on_submit():
        statusid=int(roomform.status.data)
        if roomform.submit_roomadd.data:
            response = requests.post(request.host_url + "addhotelroom", json={
                "number": roomform.number.data,
                "beds": roomform.beds.data,
                "kitchen": roomform.kitchen.data,
                "price": roomform.price.data,
                "hotel_id": hid,
                "status_id": statusid
            }, headers=headers)
            if response.status_code == 200:
                flash("Room added successfully")
            else:
                flash("Room add failed")

        elif roomform.submit_roomupdate.data:
            response = requests.put(request.host_url + "updateroom/" + str(roomform.roomid.data), json={
                "number": roomform.number.data,
                "beds": roomform.beds.data,
                "kitchen": roomform.kitchen.data,
                "price": roomform.price.data,
                "hotel_id": hid,
            }, headers=headers)
            requests.put(request.host_url + "roomstatus/" + str(roomform.roomid.data), json={"status_id": statusid}, headers=headers)
            if response.status_code == 200:
                flash("Room updated successfully")
            else:
                flash("Room update failed")

        elif roomform.submit_roomdelete.data:
            response = requests.put(request.host_url + "deleteroom/" + str(roomform.roomid.data), headers=headers)
            if response.status_code == 200:
                flash("Room deleted successfully")
            else:
                flash("Room delete failed")
        return redirect(url_for('main.rooms', hid=hid))


    roomsearchform = RoomSearchForm()
    if roomsearchform.validate_on_submit() and roomsearchform.submit_search.data:
        return redirect(url_for('main.rooms', hid=hid, start_date=roomsearchform.start_date.data, end_date=roomsearchform.end_date.data))

    serviceform = ServiceForm()
    if serviceform.validate_on_submit():
        if serviceform.submit_seradd.data:
            response = requests.post(request.host_url + "services", json={
                "name": serviceform.name.data,
                "price": serviceform.price.data,
                "hotel_id": hid
            }, headers=headers)
            if response.status_code == 200:
                flash("Service added successfully")
            else:
                flash("Service add failed")
            
        elif serviceform.submit_serupdate.data:
            response = requests.put(request.host_url + "services/" + str(serviceform.serviceid.data), json={
                "name": serviceform.name.data,
                "price": serviceform.price.data,
            }, headers=headers)
            if response.status_code == 200:
                flash("Service updated successfully")
            else:
                flash("Service update failed: ")

        elif serviceform.submit_serdelete.data:
            response = requests.delete(request.host_url + "services/" + str(serviceform.serviceid.data), headers=headers)
            if response.status_code == 200:
                flash("Service deleted successfully")
            else:
                flash("Service delete failed")    
        return redirect(f"/rooms/{hid}")

    reviewform = ReviewForm()
    if reviewform.validate_on_submit() and reviewform.submitreview.data:
        response = requests.post(request.host_url + "review/add", json={
            "hotel_id": int(hid),
            "rating": reviewform.rating.data,
            "comment": reviewform.comment.data
        }, headers=headers)
        if response.status_code == 200:
            flash("Review added successfully")
        else:
            msg = response.json().get('message', response.text)
            flash(f"Review add failed: {msg}")
        return redirect(url_for('main.rooms', hid=hid))

    reserveForm = ReserveForm()
    reserveForm.roomid.choices = [(room['id'], f"Szoba {room['number']}") for room in availableRooms]
    if reserveForm.validate_on_submit() and reserveForm.submit_reservation.data:
        if start_date and end_date:
            response = requests.post(request.host_url + "reservation/add", json={
                "room_ids": reserveForm.roomid.data,
                "reserved_start_date": start_date,
                "reserved_end_date": end_date
            }, headers=headers)
            if response.status_code == 200:
                flash("Reservation added successfully")
            else:
                msg = response.json().get('message', response.text)
                flash(f"Failed to add reservation: {msg}")
        else:
            flash(f"Need start and end dates")
        return redirect(url_for('main.rooms', hid=hid, start_date=start_date, end_date=end_date))



    return render_template(
        'rooms.html', 
        rooms=rooms, user=user, roles=roles, hid=hid, 
        services=services,  reviewform=reviewform,
        roomform=roomform, roomsearch=roomsearchform, 
        serviceform=serviceform, reserveform = reserveForm
    )



@bp.route('/personalinvoice', methods=['GET', 'POST'])
def invoice():
    user = get_user_from_session()
    roles = []
    headers = {}
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()
        headers = {'Authorization': f"Bearer {user['token']}"}
    response = requests.get(request.host_url + "/invoice/mine", headers=headers)
    invoices = response.json()
    return render_template('invoice.html', invoices=invoices, user=user)



@bp.route('/reception', methods=['GET', 'POST', 'PUT'])
def reception():
    user = get_user_from_session()
    roles = []
    headers = {}
    if user:
        roles = requests.get(request.host_url + "userroles", headers={'Authorization': f"Bearer {user['token']}"}).json()
        headers = {'Authorization': f"Bearer {user['token']}"}
    response = requests.get(request.host_url + "/reservations/pending", headers=headers)
    reception = response.json()
    return render_template(
        'reception.html',
        reception=reception,
        user=user
    )