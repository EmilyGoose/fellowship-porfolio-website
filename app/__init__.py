import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_nav import Nav, register_renderer
from flask_nav.elements import Navbar, View
from peewee import MySQLDatabase, Model, DateTimeField, TextField, CharField
import datetime

from playhouse.shortcuts import model_to_dict

from generate_map import generate_map
from navbar_renderer import NavbarRenderer

load_dotenv()
app = Flask(__name__)

# Initiate MySQL database
mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = mydb


# Connect to the DB and create table for the app
mydb.connect()
mydb.create_tables([TimelinePost])

# Create dynamic navbar instance
nav_bar = Navbar('Navigation',
                 View('Home', 'index'),
                 View('Work Experience', 'experience'),
                 View('Hobbies', 'hobbies'),
                 View('Timeline', 'timeline')
                 )

# Initialize and register Nav library
nav = Nav()
nav.register_element('navigation', nav_bar)
nav.init_app(app)
# Register the custom navbar renderer
register_renderer(app, 'navbar', NavbarRenderer)

# Load the JSON data with group member info
json_path = os.path.join(app.root_path, "static/data", "group.json")
json_data = json.load(open(json_path))

# Check if templates/generated exists, if not create the folder
folder_path = os.path.join(app.root_path, "templates/generated")
if not os.path.isdir(folder_path):
    os.mkdir(folder_path)

# Generate the Folium map HTML
generate_map(os.path.join(app.root_path, "templates/generated", "generated_map.html"), json_data)


@app.route('/')
def index():
    return render_template('index.html', json_data=json_data, title="About Us", url=os.getenv("URL"))


@app.route('/experience')
def experience():
    return render_template('experience.html', json_data=json_data, title="Work Experience", url=os.getenv("URL"))


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', json_data=json_data, title="Hobbies", url=os.getenv("URL"))


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", posts=get_posts()['timeline_posts'])


# This route is only used in an iframe, so it doesn't need to be on the navbar
@app.route('/map')
def travel_map():
    return render_template('generated/generated_map.html')


# Create post endpoint
@app.route('/api/timeline_post', methods=['POST'])
def post_post():
    print(request.values.to_dict())
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_posts():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
