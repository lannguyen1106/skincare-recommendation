"""
This module is the Flask blueprint for the product catalog page (/).
"""


from flask import Blueprint, render_template

home_page = Blueprint('home_page', __name__)


@home_page.route('/')
# @auth_optional
def hello():
    
    return render_template('landing.html')


@home_page.route('/hello')
# @auth_optional
def display():
    
    return render_template('home.html',) 
                      
