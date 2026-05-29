from flask import render_template, request, flash, redirect, session
from Hotelguru.blueprints.main import bp
import requests
from Hotelguru.Forms.loginForm import LoginForm


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

@bp.route('/rooms/<hid>')
def rooms(hid):
    api_url = request.host_url + "listrooms/" + hid
    response = requests.get(api_url)
    rooms = response.json()
    user = session.get('user')
    return render_template('rooms.html', rooms=rooms, user=user)
