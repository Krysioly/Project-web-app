from server import app
import unittest, json
from model import db, connect_to_db, Entry, User, Todo
from selenium import webdriver
import server


class JournalTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        example_data()
        server.get_weather = mock_weather_api
        server.get_quote = mock_quote_api

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        print("\n test homepage \n")
        result = self.client.get("/")
        self.assertIn(b"Daily Journal", result.data)

    def test_login(self):
        print("\n test login \n")
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b'<img src="static/img/journal.jpg">', dashresult.data)
        self.assertIn(b'<div class="card-header">', dashresult.data)
        self.assertNotIn(b"Log In User", dashresult.data)

    def test_wrong_password(self):
        print("\n test wrong password \n")
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "notpass"},
                                follow_redirects=True)
        self.assertIn(b"Log In User", result.data)
        self.assertNotIn(b'<img src="static/img/journal.jpg">', result.data)

    def test_wrong_login(self):
        print("\n test wrong login \n")
        result = self.client.post("/check-login", 
                                data={'email': "notbright@email.com", 'password': "notpass"},
                                follow_redirects=True)
        logresult = self.client.get("/register")
        self.assertIn(b"Register New User", logresult.data)
        self.assertNotIn(b'<img src="static/img/journal.jpg">', logresult.data)

    def test_bright_entries(self):
        print("\n test bright entries \n")
        result = self.client.post("/check-login", 
                                data={'email': "brighticorn@email.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b'<img src="static/img/journal.jpg">', dashresult.data)
        entryresult = self.client.get("/entries")
        self.assertIn(b"Entry Title", entryresult.data)
        self.assertNotIn(b"Testing same date", entryresult.data)


    def test_pair_entries(self):
        print("\n test pair entries \n")
        result = self.client.post("/check-login", 
                                data={'email': "pair@programmer.com", 'password': "abc123"},
                                follow_redirects=True)
        self.assertIn(b'<img src="static/img/journal.jpg">', result.data)
        entryresult = self.client.get("/entries")
        self.assertIn(b"Testing same date", entryresult.data)
        self.assertNotIn(b"Entry Title", entryresult.data)

    def test_bright_todo(self):
        print("\n test bright todo\n")
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b"laundry", dashresult.data)
        self.assertNotIn(b"sweep/mop", dashresult.data)

    def test_pair_todo(self):
        print("\n test pair todo \n")
        result = self.client.post("/check-login", 
                                data={'email': "pair@programmer.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b"sweep/mop", dashresult.data)
        self.assertNotIn(b"laundry", dashresult.data)
    
    def test_weather_api(self):
        print("\n test weather \n")
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b'<img src="static/img/journal.jpg">', dashresult.data)
        self.assertIn(b'Rain', dashresult.data)
    
    def test_quote_api(self):
        print("\n test quote \n")
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "abc123"},
                                follow_redirects=True)
        dashresult = self.client.get("/dashboard")
        self.assertIn(b'<img src="static/img/journal.jpg">', dashresult.data)
        self.assertIn(b"Be daring, be different, be impractical, be anything that will assert integrity of purpose and imaginative vision against the playitsafers, the creatures of the commonplace, the slaves of the ordinary.",
            dashresult.data)


def mock_weather_api():
    weather_json = open("weather.json").read()
    weather_info = json.loads(weather_json)
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

def mock_quote_api():
    quote_json = open("quote.json").read()
    quote_info = json.loads(quote_json)
    quote = quote_info["contents"]["quotes"][0]["quote"]

    return quote

def example_data():
    Entry.query.delete()
    Todo.query.delete()
    User.query.delete()
    
    #users
    brighticorn = User(name='Brighticorn', user_id=1, email='brighticorn@email.com', 
        password='6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', zipcode='94566')
    pairprogrammer = User(name='PairProgrammer', user_id=2, email='pair@programmer.com',
        password='6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090', zipcode='94588')
    #entries
    be1 = Entry(user_id=1, date='2018-10-3', title='Entry Title', 
        text='Entry body text', quote='Some random quote for the day', weather='Sunny')
    be2 = Entry(user_id=1, date='2018-10-4', title='Another Title', 
        text='Some text to go in entry body', quote='another quote', weather='Cloudy')
    pe1 = Entry(user_id=2, date='2018-10-3', title='Testing same date',
        text='Enrty body for testing same date', quote='some quote', weather='Snowy')
    pe2 = Entry(user_id=2, date='2018-10-16', title='Test Title', 
        text='Some text for an entry body', quote='daily quote', weather='Sunny')
    #todo
    bt1 = Todo(user_id=1, todo_id=1, todo='wash dishes')
    bt2 = Todo(user_id=1, todo_id=2, todo='laundry')
    pt1 = Todo(user_id=2, todo_id=3, todo='sweep/mop')

    db.session.add_all([brighticorn, pairprogrammer, be1, be2, pe1, pe2, bt1, bt2, pt1])
    db.session.commit()
    

if __name__ == "__main__":
    unittest.main()

