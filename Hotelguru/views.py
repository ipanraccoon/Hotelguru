"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from apiflask import APIBlueprint

bp = APIBlueprint('main', __name__)



@bp.route('/')
@bp.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'Hotelgurumain.html',
        title='Home Page',
        year=datetime.now().year,
    )

@bp.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@bp.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
