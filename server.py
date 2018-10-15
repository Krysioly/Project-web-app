""" Daily Journal """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import requests, json, datetime, calendar 
# from pyowm import OWM
import os
from model import connect_to_db, db, User, Entry, Todo

app = Flask(__name__)

app.secret_key = "password"
app.jinja_env.undefined = StrictUndefined

weather_key = os.environ['weather_key']
# owm = OWM(weather_key)
# from pyowm.caches.lrucache import LRUCache
# cache = LRUCache()

############# ROUTES ######################
@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


############ Register/ logging ##############
@app.route('/register')
def register_user_form():
    """Make a new User"""

    return render_template("register_form.html")


@app.route('/check-register', methods=['POST'])
def check_user_register():
    """Check if user is new and create db entry"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if User.query.filter_by(email = user_email).first() is None:
        new_user = User(email=user_email, password=user_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You were successfully registered')
        return redirect('/')

    else:
        flash('You are already a user, try logging in')
        return redirect('/login')


@app.route('/login')
def login_user_form():
    """Log user in"""

    return render_template('login_form.html')


@app.route('/check-login', methods=['POST'])
def check_user_login():
    """Check if user is valid and log in"""

    login_email = request.form.get('email')
    login_password = request.form.get('password')
    login_user = User.query.filter_by(email = login_email).first()

    if session.get('email') is None:
        if login_user:
            if login_user.password == login_password:
                flash('You were successfully logged in')
                session['email'] = login_email
                session['password'] = login_password
                return redirect('/dashboard')

            else:
                flash('Your email does not match your password')
                return redirect('/login')
        else:
            flash('You were not found, try registering')
            return redirect('/register-user')
    else:
        flash('You have already logged in')
        return redirect('/')


@app.route('/logout', methods = ['POST'])
def logout_user():
    """Log the user out"""

    if session.get('email'):
        del session['email']
        del session['password']
        flash('You were logged out')
        return redirect('/')
    else:
        flash('You were not logged in')
        return redirect('/login')


################# Entries #####################

@app.route("/dashboard")
def show_dashboard_form():
    """Show dashboard with form"""

    if session.get("email"):
        quote = get_quote()
        weathers = get_weather()
        img_src = change_weather_img(weathers["description"])
        finduser = User.query.filter_by(email=session["email"]).first()
        todo_list = Todo.query.filter_by(user_id = finduser.user_id).all()
        today = datetime.date.today()
        current_entry = Entry.query.filter_by(date = today).first()

        return render_template("dashboard.html", quote = quote,
                weathers = weathers, img_src = img_src, 
                todo_list = todo_list, current_entry=current_entry)
    else:
        flash("You need to log in to see your Dashboard Page")
        return redirect("/login") 


@app.route("/post-entry", methods=["POST"])
def submit_form():
    """Save entry into database"""

    today = datetime.date.today()
    finduser = User.query.filter_by(email=session["email"]).first()

    title = request.form.get("title")
    text = request.form.get("text")
    
    new_entry = Entry(title = title, text = text, date = today,
        user_id = finduser.user_id)
    db.session.add(new_entry)
    db.session.commit()
    results = {"title": title, "text": text}
    return jsonify(results)


@app.route("/update-todo", methods=["POST"])
def update_todo():
    """Update to do list"""

    todo = request.form.get("todo")
    finduser = User.query.filter_by(email=session["email"]).first()
    new_todo = Todo(user_id= finduser.user_id, todo= todo)
    db.session.add(new_todo)
    db.session.commit()

    return todo


@app.route("/delete-todo", methods=["POST"])
def delete_todo():
    delete = request.form.get("todoItem")
    print("\n\n",delete,"\n\n")
    done_todo = Todo.query.filter_by(todo=delete).first()
    db.session.delete(done_todo)
    db.session.commit()
    
    return delete


@app.route("/calendar")
def show_calendar():
    """Show dashboard page"""

    # c = calendar.HTMLCalendar(calendar.SUNDAY)
    # str = c.formatmonth(2018, 10)
    # print(str)
    return render_template("calendar.html")#, calendar = str)


@app.route("/entry")
def show_previous_entry():
    """Show dashboard page"""
    if session.get("email"):    
        finduser = User.query.filter_by(email=session["email"]).first()
        entries = Entry.query.filter_by(user_id=finduser.user_id).all()

        return render_template("previous-entry.html", entries = entries)
    else:
        flash("You need to sign in to see your Previous Entries")
        return redirect("/login")


#########################################################

def get_quote():
    """ qoute api """

    # responseQ = requests.get("http://quotes.rest/qod", {"Accept": "application/json"})
    # quote_json = responseQ.text
    quote_json = open("quote.json").read()
    quote_info = json.loads(quote_json)

    quote = quote_info["contents"]["quotes"][0]["quote"]

    return quote

def get_weather():
    """ weather api """

    user = User.query.filter_by(email=session["email"]).first()
    
    # weather = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + user.zipcode+"&APPID="+weather_key)
    # weather_json = weather.text
    weather_json = open("weather.json").read()

    weather_info = json.loads(weather_json)
    weather_desc = weather_info["weather"][0]["description"]

    temp = weather_info["main"]["temp"]
    weather_temp = round((1.8 * (temp - 273)) + 32)

    temp_min = weather_info["main"]["temp_min"]
    weather_temp_min = round((1.8 * (temp_min - 273)) + 32)

    temp_max = weather_info["main"]["temp_max"]
    weather_temp_max = round((1.8 * (temp_max - 273)) + 32)
    #make into dictionary
    weather_dictionary = {"description" : weather_desc, "temp":weather_temp,
        "temp_min": weather_temp_min, "temp_max": weather_temp_max}




    return weather_dictionary


def change_weather_img(weather):
    """Change weather picture to match weather info"""

    if "rain" in weather:
        return "static/img/rainy.jpg"
    elif "drizzle" in weather:
        return "static/img/rainy.jpg"
    elif "snow" in weather:
        return "static/img/snowy.jpg"
    elif "sun" in weather:
        return "static/img/sunny.jpg"
    elif "clear" in weather:
        return "static/img/sunny.jpg"
    elif "partly" in weather:
        return "static/img/partly-cloudy.jpg"
    elif "broken" in weather:
        return "static/img/partly-cloudy.jpg"
    elif "cloud" in weather:
        return "static/img/cloudy.jpg"
    elif "lightening" in weather:
        return "static/img/lightening.jpg"
    elif "tornado" in weather:
        return "static/img/tornado.jpg"




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
