
from flask import render_template
from .slayer_app import SlayerApp

print('Initializing Slayer Intro Handler...')
num_opening_pages = 3

@SlayerApp.route("/narrative/<int:page>")
def narrative(page):
    return render_template("narrative" + str(page) + ".html", previous_page = str(page - 1), next_page = str(page + 1), has_previous_page = page > 1, has_next_page = page < num_opening_pages)
