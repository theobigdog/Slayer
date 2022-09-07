
from flask import Flask, redirect, url_for, escape, render_template, flash, request
from flask_login import LoginManager, login_required

from slayer_server.items.item_manager import ItemManager

from .party.party_manager import PartyManager
from .user_manager import UserManager
from .slayer_files import Slayer_Root
from .adventures.adventure_manager import AdventureManager
import sys

import flask_login

print('Initializing slayer app...')
Slayer_Version = 3

SlayerApp = Flask(__name__, static_url_path = '', static_folder = Slayer_Root + '/static_html', template_folder = Slayer_Root + '/templates')
SlayerApp.config['TEMPLATES_AUTO_RELOAD'] = True
SLayerItemDB = ItemManager()
PartyManager()
#AdventureManager()

SlayerApp.secret_key = 'shhhhh this is a secret'

SlayerLoginManager = LoginManager()
SlayerLoginManager.init_app(SlayerApp)

SlayerUserManager = UserManager()

@SlayerLoginManager.user_loader
def load_user(user_id):
  return SlayerUserManager.lookup_user(user_id)

# Defines the route for the starting page for the slayer experience
@SlayerApp.route("/")
@flask_login.login_required
def get_home_page():
  flash('Welcome, ' + flask_login.current_user.name + '!  Prepare to Die!')
  return render_template('start_page.html', version = Slayer_Version, bg_img = "Introduction_b&w_best.jpg")

# Authorize the new user connection.  Check to see if the user is already authorized and if so just
# redirect.  If not authorized, attempt to perform authorization and register the user upon success.
@SlayerApp.route('/get_authorized')
def get_authorized():
  print('Request authorization!')
  print(flask_login.current_user)

  if flask_login.current_user.is_authenticated != True:
    user = SlayerUserManager.establish_user()
    flask_login.login_user(user)
    print('User: ID=' + flask_login.current_user.get_id() + ', Auth=' + str(flask_login.current_user.is_authenticated) + ', Name=' + flask_login.current_user.name)
    flash('You didn\'t provide a name.  I think I\'ll call you... ' + flask_login.current_user.name)
  else:
    print('Already authorized, redirecting ' + flask_login.current_user.name + ' to authtest')
    sys.stdout.flush()
    return redirect(url_for('get_home_page'))

  next = request.args.get('next')
  print('next is [' + str(next) + ']')
  sys.stdout.flush()
  return redirect(next or url_for('get_home_page'))


# Endpoint to be directed to is authorization is required but fails for any reason.  Display an
# error indicating that authorization failed and provide available instructions or help for the user to
# get authorized
@SlayerApp.route('/not_authorized')
def auth_failed():
  return "Authorization failure is complete."


# Configure the function to notify if an endpoint is requested that requires requires authentication
# (uses the @flask_login.login_required decoration).  This happens the first time a user connects to
# the server and this function redirects the browser to the authorization page.
@SlayerLoginManager.unauthorized_handler
def unauthorized_handler():
  print('flask login unauthorized!')
  return redirect(url_for('get_authorized'))


# Handle an HTTP 401 error.  401 is code for Not Authorized.  If the code is due to an endpoint that
# needs authorization then the unauthorized_handler() above should have been called.  If it is not for
# some reason then this function serves as a backup.
@SlayerApp.errorhandler(401)
def not_authorized(e):
  return redirect('/get_authorized')

# Handle an HTTP 404 error.  404 is code for Resource Not Found.
@SlayerApp.errorhandler(404)
def page_not_found(e):
  return render_template("error_page.html", msg = str(e))


from . import *
