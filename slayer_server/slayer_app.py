
from flask import Flask, session, redirect, url_for, escape, render_template
# from flask_session import Session

print('Initializing slayer app...')

Slayer_Version = 3

SlayerApp = Flask(__name__, static_url_path = '', static_folder = '../static_html', template_folder = '../templates')

@SlayerApp.route("/")
def get_home_page():
    return render_template('start_page.html', version = Slayer_Version)

@SlayerApp.errorhandler(404)
def page_not_found(e):
    return render_template("error_page.html", msg = str(e))

from . import *
