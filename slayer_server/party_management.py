
from logging import NullHandler
from flask import  render_template, request, redirect
from .slayer_app import SlayerApp
import pandas as pd
from os.path import exists

print('Initializing party management ...')

# hero_classes = ['Warrior', 'Shifter', 'Battle-Mage', 'Hunter', 'Wizard', 'Sapper', 'Cleric']

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
    filename = 'saves/' + request.form['filename']
    file_exists = exists(filename)
    if file_exists:
        party = pd.read_json('saves/' + request.form['filename']) #load_party_json
        return render_template("display_party.html", party = party)
    else:
        return redirect('/get_party/File%20Not%20Found')

@SlayerApp.route("/query_update_names")
def query_update_names():
    return render_template("query_update_names.html")

@SlayerApp.route("/save_game1")
def save_game1():
    return render_template("save_game1.html")

@SlayerApp.route("/save_game2/", methods=['POST'])
def save_game2():
    save_name = request.form['save_name']
    if not save_name.endswith('.json'):
        save_name += '.json'
    temp = pd.read_json('saves/test.json') ### This needs to be fixed so proper file is loaded
    temp.to_json('saves/' + save_name) ### This needs to be fixed so proper file is saved
    return render_template("save_game2.html")

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