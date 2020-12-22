import os
from flask import (
    Flask, flash, render_template, redirect,
    request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, date

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """
    Renders home page template when going to the main website link
    """
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign up - This function allows the user to register on the Sign Up page.
    If the username already exists in the DB a flash message will
    display to alert the user.
    If the username does not exist and registration was successful,
    the user will be logged in, redirected to the profile page
    and a flash message displayed to verify it was successful.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("This user name already exists.", 'error')
            return redirect(url_for("signup"))

        newUser = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "name": request.form.get("name").lower()
        }
        mongo.db.users.insert_one(newUser)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!", 'message')
        return redirect(url_for(
                    "profile", username=session["user"]))

    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """
    Sign In - Function checks if username exists in 'users' database
    If user name  exists and hashed password matches user input -
    User is logged in, welcome message displayed and user redirected
    to their profile.
    If incorrect username or password, user is redirected to sign in
    and a flash message displayed alerting of inccorect username/password.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f"Welcome, {session['user']}", 'message')
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password", 'error')
                return redirect(url_for("signin"))

        else:
            flash("Incorrect Username and/or Password", 'error')
            return redirect(url_for("signin"))

    return render_template("signin.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Takes the session user's username from 'users' database
    and returns them to their profile page. Returns events
    created by the user.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        events = list(mongo.db.events.find().sort("date"))
        return render_template("profile.html",
                               username=username, events=events)

    return redirect(url_for("signin"))


@app.route("/signout")
def signout():
    """
    Removes logged in user from session cookie and
    returns them to the signin page.
    """
    flash("You have been signed out", 'message')
    session.pop("user")
    return redirect(url_for("signin"))


@app.route("/contact")
def contact():
    """
    Renders contact template
    """
    return render_template("contact.html")


@app.route("/events")
def get_events():
    """
    Reads all entries in the collection, iterates through them and converts
    the events date into a date object. If the events date is greater than
    todays date, it's added to the events list.
    events is then sorted on date and the first 6 items saved back to events.
    Dates are then converted back to strings and events list returned.
    Passes categories list in to poplate event type drop down.
    """
    all_events = list(mongo.db.events.find())
    categories = mongo.db.categories.find().sort("event_type", 1)
    todays_date = date.today()
    events = list()

    for event in all_events:
        event_date = datetime.strptime(event.get('date'), '%d %B %Y').date()
        if event_date > todays_date:
            event['date'] = event_date
            events.append(event)
    events.sort(key=lambda x: x['date'])

    events = events[:6]

    for event in events:
        event['date'] = datetime.strftime(event.get('date'), '%d %B %Y')
    return render_template("events.html", events=events, categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Returns search results from user input query or drop down
    selection from events page.
    Iterates through events returned and converts dates to date objects
    in order to sort by date ascending. Converts back to strings after.
    Renders template for events.html.
    """
    query = request.form.get("query")
    event_type = request.form.get("event_type")
    events = list()
    if query:
        events = list(mongo.db.events.find({"$text": {"$search": query}}))
    elif event_type:
        events = list(mongo.db.events.find({"$text": {"$search": event_type}}))

    for event in events:
        event_date = datetime.strptime(event.get('date'), '%d %B %Y').date()
        event['date'] = event_date
    events.sort(key=lambda x: x['date'])

    for event in events:
        event['date'] = datetime.strftime(event.get('date'), '%d %B %Y')

    categories = mongo.db.categories.find().sort("event_type", 1)
    return render_template("events.html", events=events, categories=categories)


@app.route("/create-event", methods=["GET", "POST"])
def create_event():
    """
    Gets form values from create event and stores into event object
    when form submits.
    Inserts record into events collection and shows flash message of success.
    Returns categories to create_events page to populate drop downs on form.
    """
    if request.method == "POST":
        event = {
            "event_type": request.form.get("event_type"),
            "location": request.form.get("location"),
            "date": request.form.get("date"),
            "description": request.form.get("description"),
            "organiser": request.form.get("organiser"),
            "created_by": session["user"]
        }
        mongo.db.events.insert_one(event)
        flash("Event Successfully Created", 'message')
        return redirect(url_for("create_event"))

    categories = mongo.db.categories.find().sort("event_type", 1)
    return render_template("create-event.html", categories=categories)


@app.route("/edit-event/<event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    """
    Allows user to edit an event. If successful, flash message is displayed
    to alert user.
    """
    if request.method == "POST":
        submit = {
            "event_type": request.form.get("event_type"),
            "location": request.form.get("location"),
            "date": request.form.get("date"),
            "description": request.form.get("description"),
            "organiser": request.form.get("organiser"),
            "created_by": session["user"]
        }
        mongo.db.events.update({"_id": ObjectId(event_id)}, submit)
        flash("Event Successfully Updated", 'message')

    event = mongo.db.events.find_one({"_id": ObjectId(event_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit-event.html",
                           event=event, categories=categories)


@app.route("/delete_event/<event_id>")
def delete_event(event_id):
    """
    Allows user to delete  an event. Returns user back to
    their profile page.
    """
    mongo.db.events.remove({"_id": ObjectId(event_id)})
    flash("Event Successfully Deleted", 'message')

    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return redirect(url_for("profile", username=username))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
