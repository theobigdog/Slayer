
from flask import Flask, session, redirect, url_for, escape, render_template
from flask_login import LoginManager, login_required
import sys

import flask_login
# from flask_session import Session

print('Initializing slayer app...')

Slayer_Version = 3

SlayerApp = Flask(__name__, static_url_path = '', template_folder = '../templates')

SlayerLoginManager = LoginManager()
SlayerLoginManager.init_app(SlayerApp)

@SlayerLoginManager.user_loader
def load_user(user_id):
  print('Request to load user, ID=')
  print(user_id)
  sys.stdout.flush()
  return None

@SlayerApp.route("/")
def get_home_page():
  print('Request home page!')
  print(flask_login.current_user)
  print('authenticated: ' + str(flask_login.current_user.is_authenticated))
  print('anonymous: ' + str(flask_login.current_user.is_anonymous))
  print('id: ' + str(flask_login.current_user.get_id()))
  flask_login.login_user(user)
  sys.stdout.flush()
  return render_template('start_page.html', version = Slayer_Version)

@SlayerApp.errorhandler(404)
def page_not_found(e):
  return render_template("error_page.html", msg = str(e))

from . import *
