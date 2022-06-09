
from flask import  render_template
from .slayer_app import SlayerApp
import pandas as pd

print('Initializing party management ...')

hero_classes = ['Warrior', 'Shifter', 'Battle-Mage', 'Hunter', 'Wizard', 'Sapper', 'Cleric']

@SlayerApp.route("/party_choice")
def party_choice():
    return render_template("party_choice.html")

@SlayerApp.route("/party_generation")
def party_generation():
    return render_template("party_generation.html", party = mock_party)

@SlayerApp.route("/get_party")
def get_party():
    return render_template("get_party.html")

@SlayerApp.route("/display_party/")
def display_party():
    return render_template("display_party.html", party = load_party_json)

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

load_party_json = pd.read_json('saves/Ruxpin.json')
