
from logging import NullHandler
from flask import  render_template, request, redirect, flash
from .slayer_app import SlayerApp
import pandas as pd
from os.path import exists

print('Initializing party management ...')

# hero_classes = ['Warrior', 'Shifter', 'Battle-Mage', 'Hunter', 'Wizard', 'Sapper', 'Cleric']

def get_save_path(filename):
    path = 'saves/' + filename
    if not path.endswith('.json'):
        path = path + '.json'
    return path

@SlayerApp.route("/party_choice")
def party_choice():
    return render_template("party_choice.html")

@SlayerApp.route("/party_generation")
def party_generation():
    return render_template("party_generation.html", party = mock_party)

@SlayerApp.route("/get_party", defaults={'message': ''})
@SlayerApp.route("/get_party/<message>")
def get_party(message):
    return render_template("get_party.html", message=message)

@SlayerApp.route("/display_party/", methods=['POST'])
def display_party():
    savename = get_save_path(request.form['filename'])
    file_exists = exists(savename)
    if file_exists:
        party = pd.read_json(savename)
        return render_template("display_party.html", party = party, filename = request.form['filename'], bg_img="LoadParty-removebg_b&w_best.png")
    else:
        return redirect('/get_party/File%20Not%20Found')

@SlayerApp.route("/query_update_names", methods=['POST'])
def query_update_names():
    return render_template("query_update_names.html", filename= request.form["filename"])

@SlayerApp.route("/save_game1", methods=['POST'])
def save_game1():
    return render_template("save_game1.html", filename= request.form["filename"])

@SlayerApp.route("/save_game2/", methods=['POST'])
def save_game2():
    save_name = get_save_path(request.form['save_name'])
    file_exists = exists(save_name)
    if file_exists:
        return render_template("confirm_name.html", save_name = request.form['save_name'])
    load_name = get_save_path(request.form['filename'])
    temp = pd.read_json(load_name) ### This needs to be fixed so proper file is loaded
    temp.to_json(save_name) ### This needs to be fixed so proper file is saved
    flash("Your game has been saved.  Please record for future retrieval.  Or don't.  I don't really care.")
    return render_template("query_update_names.html")

@SlayerApp.route("/update_names")
def update_names():
    return render_template("update_names.html")

@SlayerApp.route("/begin_game")
def begin_game():
    return render_template("begin_game.html")

mock_party = [
    {
        'name' : "Bubba",
        'class' : 'something'
    },
    {
        'name' : 'Theodore',
        'class' : 'Savior'
    }
]