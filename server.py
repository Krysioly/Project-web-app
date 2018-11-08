""" Daily Journal """

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from newsapi import NewsApiClient
from model import connect_to_db, db, User, Entry, Todo
import requests, json, datetime, calendar, os
import hashlib

app = Flask(__name__)

app.secret_key = "password"
app.jinja_env.undefined = StrictUndefined

weather_key = os.environ['weather_key']
news_key = os.environ['news_key']
newsapi = NewsApiClient(api_key=news_key)


############# ROUTES ######################

@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route("/dashboard")
def show_dashboard_form():
    """Show dashboard (main page)"""

    if session.get("email"):
        calendar = make_calendar()
        quote = get_quote()
        weathers = get_weather()
        img_src = change_weather_img(weathers["main"])
        finduser = User.query.filter_by(email=session["email"]).first()
        todo_list = Todo.query.filter_by(user_id = finduser.user_id).all()
        today = datetime.date.today()
        current_entry = Entry.query.filter_by(date = today).first()

        return render_template("dashboard.html", quote=quote,
                weathers=weathers, img_src=img_src, calendar=calendar,
                todo_list=todo_list, current_entry=current_entry, user=finduser)
    else:
        flash("You need to log in to see your Dashboard Page")
        return redirect("/login") 


@app.route("/about")
def show_about_me():
    """Show user about app"""

    return render_template("about.html")


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
    login_password=login_password.encode()
    hash_password = hashlib.sha256(login_password)
    hash_password = hash_password.hexdigest()

    user_zipcode = request.form.get('zipcode')
    user_name = request.form.get('name')

    if User.query.filter_by(email = user_email).first() is None:
        new_user = User(name=user_name, email=user_email, password=hash_password, zipcode=user_zipcode)
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
    login_password=login_password.encode()
    hash_password = hashlib.sha256(login_password)
    hash_password = hash_password.hexdigest()
    login_user = User.query.filter_by(email = login_email).first()

    if session.get('email') is None:
        if login_user:
            if login_user.password == hash_password:
                flash('You were successfully logged in')
                print(hash_password)
                session['email'] = login_email
                return redirect('/dashboard')
            else:
                flash('Your email does not match your password')
                return redirect('/login')
        else:
            flash('You were not found, try registering')
            return redirect('/register')
    else:
        flash('You have already logged in')
        return redirect('/')


@app.route('/logout', methods = ['POST'])
def logout_user():
    """Log the user out"""

    if session.get('email'):
        del session['email']
        flash('You were logged out')
        return redirect('/')
    else:
        flash('You were not logged in')
        return redirect('/login')


################# Entries #####################

@app.route("/post-entry", methods=["POST"])
def submit_form():
    """Save entry into database"""

    today = datetime.date.today()
    finduser = User.query.filter_by(email=session["email"]).first()
    title = request.form.get("title")
    text = request.form.get("text")
    weather = request.form.get("weather")
    quote = request.form.get("quote")
    
    new_entry = Entry(weather=weather, quote=quote, title=title,
        text=text, date=today, user_id=finduser.user_id)
    db.session.add(new_entry)
    db.session.commit()
    results = {"title": title, "text": text}
    return jsonify(results)


@app.route("/entries")
def show_previous_entry():
    """Show older entries page"""

    if session.get("email"):    
        finduser = User.query.filter_by(email=session["email"]).first()
        print(finduser.password,"\n\n")
        entries = Entry.query.filter_by(user_id=finduser.user_id).order_by(Entry.date.desc()).all()

        return render_template("previous-entry.html", entries=entries, user=finduser)
    else:
        flash("You need to sign in to see your Previous Entries")
        return redirect("/login")


@app.route("/entry-data.json")
def get_entry_data():
    """Chart data based on the database"""

    finduser = User.query.filter_by(email=session["email"]).first()
    entries = Entry.query.filter_by(user_id=finduser.user_id).order_by(Entry.date).all()
    jan=0
    feb=0
    mar=0
    apr=0
    may=0
    jun=0
    jul=0
    aug=0
    sept=0
    octo=0
    nov=0
    dec=0
    for entry in entries:
        date= datetime.datetime.strptime(str(entry.date), "%Y-%m-%d")
        if date.month == 1:
            jan+=1
        elif date.month == 2:
            feb+=1
        elif date.month == 3:
            mar+=1
        elif date.month == 4:
            apr+=1
        elif date.month == 5:
            may+=1
        elif date.month == 6:
            jun+=1
        elif date.month == 7:
            jul+=1
        elif date.month == 8:
            aug+=1
        elif date.month == 9:
            sept+=1
        elif date.month == 10:
            octo+=1
        elif date.month == 11:
            nov+=1
        elif date.month == 12:
            dec+=1
    data_dict = { 
        "labels": [
            "January", "February", "March", "April",
            "May", "June", "July", "August", "September",
            "October", "November", "December"],
        "datasets": [
            {   "label" : "Entries",
                "data": [jan, feb, mar, apr, may, jun, jul, 
                aug, sept, octo, nov, dec],
                "backgroundColor": ["#ff0000", "#990000",
                "#ff6600", "#ffff00", "#66ff33", "#006600", 
                "#00ffff", "#0000ff", "#000099", "#cc33ff",
                "#800080", "#000000"]
            }
        ]
    }
    return jsonify(data_dict)


############## Todo List #######################################

@app.route("/update-todo", methods=["POST"])
def update_todo():
    """Add todo item to database"""

    todo = request.form.get("todo")
    finduser = User.query.filter_by(email=session["email"]).first()
    new_todo = Todo(user_id= finduser.user_id, todo= todo)
    db.session.add(new_todo)
    db.session.commit()
    return todo


@app.route("/delete-todo", methods=["POST"])
def delete_todo():
    """Delete todo item from database"""

    delete = request.form.get("todoItem")
    done_todo = Todo.query.filter_by(todo=delete).first()
    db.session.delete(done_todo)
    db.session.commit()
    return delete


################ Api #############################

@app.route("/search-keyword")
def search_keyword():
    """search news articles by keyword"""

    newskeyword = request.args.get("keyword")
    all_articles = newsapi.get_everything(
        q=newskeyword, sources=None, domains=None,
        language='en', sort_by='relevancy')
    print("\n\n", all_articles,"\n\n")
    return jsonify(all_articles)


@app.route("/search-stocks", methods=["POST"])
def stocks_info():
    """ stocks api """

    time = request.form.get('time')
    symbol = request.form.get('symbol')
    stocksdata_info = requests.get('https://api.iextrading.com/1.0/stock/'+symbol+'/chart/'+time)
    stocksdata_json = stocksdata_info.json()
    stocks_info = requests.get("https://api.iextrading.com/1.0//stock/"+symbol+"/company")
    stocks_json = stocks_info.json()
    labels = []
    datas = []
    for stock in stocksdata_json:
        labels.append(stock['label']) 
        if 'close' not in stock:
            pass
        else:
            datas.append(stock['close'])
    data_dict = { 
        "labels": labels,
        "datasets": [
            {"label" : stocks_json['symbol'],
            "data": datas,
            "backgroundColor": "rgba(102,0,102,.5)",
            }
        ],
        "info": {"Symbol": stocks_json['symbol'],"Company": stocks_json['companyName'],
                "Description": stocks_json['description'], 
                "Exchange": stocks_json['exchange'], "Website": stocks_json['website'],},
    }
    return jsonify(data_dict)


#################### Functions ##################################

def make_calendar():
    """make a calendar"""

    today = datetime.date.today()
    newcalendar = calendar.HTMLCalendar(firstweekday=6)

    return newcalendar.formatmonth(today.year, today.month)


def get_quote():
    """get data for qoute api """
    
    responseQ = requests.get("http://quotes.rest/qod", {"Accept": "application/json"})
    if responseQ == '200':
        quote_info = responseQ.json()
        quote = quote_info["contents"]["quotes"][0]["quote"]
    else:
        quote = "Calm mind brings inner strength and self-confidence, so that's very important for good health."

    return quote


def get_weather():
    """get data for weather api """

    user = User.query.filter_by(email=session["email"]).first()
    
    weather = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=" + user.zipcode+"&APPID="+weather_key)
    weather_info = weather.json()
    
    weather_desc = weather_info["weather"][0]["main"]
    # change weather from kelvin to farenheight
    temp = weather_info["main"]["temp"]
    weather_temp = round((1.8 * (temp - 273)) + 32)
    temp_min = weather_info["main"]["temp_min"]
    weather_temp_min = round((1.8 * (temp_min - 273)) + 32)
    temp_max = weather_info["main"]["temp_max"]
    weather_temp_max = round((1.8 * (temp_max - 273)) + 32)

    weather_dictionary = {"main" : weather_desc, "temp":weather_temp,
        "temp_min": weather_temp_min, "temp_max": weather_temp_max}
    return weather_dictionary


def change_weather_img(weather):
    """Change weather picture to match weather info"""

    if "rain" in weather.lower():
        return "static/img/rain.png"
    elif "drizzle" in weather.lower():
        return "static/img/rain.png"
    elif "snow" in weather.lower():
        return "static/img/snow.png"
    elif "sun" in weather.lower():
        return "static/img/sun.png"
    elif "clear" in weather.lower():
        return "static/img/sun.png"
    elif "partly" in weather.lower():
        return "static/img/partly-cloudy.png"
    elif "broken" in weather.lower():
        return "static/img/partly-cloudy.png"
    elif "cloud" in weather.lower():
        return "static/img/cloudy.png"
    elif "lightening" in weather.lower():
        return "static/img/lightening.png"
    elif "thunder" in weather.lower():
        return "static/img/lightening.png"
    elif "tornado" in weather.lower():
        return "static/img/tornado.png"
    elif "haze" in weather.lower():
        return "static/img/fog.png"
    elif "fog" in weather.lower():
        return "static/img/fog.png"
    elif "smoke" in weather.lower():
        return "static/img/fog.png"
    elif "mist" in weather.lower():
        return "static/img/fog.png"


################# Run App ##########################################

if __name__ == "__main__":
    # We have to set debug=True here to invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    connect_to_db(app, 'postgresql:///journals')
    app.run(port=5000, host='0.0.0.0')
