
from flask import render_template
from .slayer_app import SlayerApp

print('Initializing party management ...')

@SlayerApp.route("/party_generation")
def party_generation():
    return render_template("party_generation.html", party = my_list)

my_list = [
    {
        'name' : "Bubba",
        'class' : 'something'
    },
    {
        'name' : 'Theodore',
        'class' : 'Savior'
    }
]
