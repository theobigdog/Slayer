Slayer_Version = 3

import flask as Flask
import pandas as pd

app = Flask.Flask(__name__, static_url_path = '', template_folder = 'templates')

num_opening_pages = 3

@app.errorhandler(404)
def page_not_found(e):
    print(str(e))
    return Flask.render_template("error_page.html", msg = str(e))  # This redirects back to root

@app.route("/")
def get_home_page():
    return Flask.render_template('start_page.html', version = Slayer_Version)

@app.route("/narrative/<int:page>")
def narrative(page):
    return Flask.render_template("narrative" + str(page) + ".html", previous_page = str(page - 1), next_page = str(page + 1), has_previous_page = page > 1, has_next_page = page < num_opening_pages)

@app.route("/party_choice")
def party_choice():
    return Flask.render_template("party_choice.html")

@app.route("/party_generation")
def party_generation():
    return Flask.render_template("party_generation.html", party = mock_party)

@app.route("/get_party")
def get_party():
    return Flask.render_template("get_party.html")

@app.route("/display_party/")
def display_party():
    return Flask.render_template("display_party.html", party = load_party_json)

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

# print(load_party_json)
# input()

app.run()
