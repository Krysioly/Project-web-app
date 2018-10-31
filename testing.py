from server import app
import unittest
from model import db, connect_to_db, Entry, User, Todo
from selenium import webdriver

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/dashboard')
        self.assertEqual(self.browser.title, 'Dashboard')

    def test_math(self):
        self.browser.get('http://localhost:5000/dashboard')

        x = self.browser.find_element_by_id('title')
        x.send_keys("Selenium Test Title")
        y = self.browser.find_element_by_id('text')
        y.send_keys("Selenium Test Text")

        btn = self.browser.find_element_by_id('publish')
        btn.click()

        resultTitle = self.browser.find_element_by_id('finishedTitle')
        self.assertEqual(resultTitle.text, "Selenium Test Title")

        resultText = self.browser.find_element_by_id('finishedText')
        self.assertEqual(resultText.text, "Selenium Test Text")


class JournalTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"Daily Journal", result.data)

    def test_login(self):
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "password"},
                                follow_redirects=True)
        self.assertIn(b'<img src="static/img/rainbow-stack-books.png">', result.data)
        self.assertIn(b'<div class="card-header">', result.data)
        self.assertNotIn(b"Log In User", result.data)

    def test_wrong_password(self):
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "notpass"},
                                follow_redirects=True)
        # self.assertIn(b"Your email does not match your password", result.data)
        self.assertIn(b"Log In User", result.data)
        self.assertNotIn(b'<img src="static/img/rainbow-stack-books.png">', result.data)

    def test_wrong_login(self):
        result = self.client.post("/check-login", 
                                data={'email': "notbright@email.com", 'password': "notpass"},
                                follow_redirects=True)
        # self.assertIn(b"You were not found, try registering", result.data)
        self.assertIn(b"Register New User", result.data)
        self.assertNotIn(b'<img src="static/img/rainbow-stack-books.png">', result.data)

    def test_bright_entries(self):
        result = self.client.post("/check-login", 
                                data={'email': "brighticorn@email.com", 'password': "password"},
                                follow_redirects=True)
        self.assertIn(b'<img src="static/img/rainbow-stack-books.png">', result.data)
        entryresult = self.client.get("/entries")
        self.assertIn(b"Entry Title", entryresult.data)
        self.assertNotIn(b"Testing same date", entryresult.data)


    def test_pair_entries(self):
        result = self.client.post("/check-login", 
                                data={'email': "pair@programmer.com", 'password': "pass123"},
                                follow_redirects=True)
        self.assertIn(b'<img src="static/img/rainbow-stack-books.png">', result.data)
        entryresult = self.client.get("/entries")
        self.assertIn(b"Testing same date", entryresult.data)
        self.assertNotIn(b"Entry Title", entryresult.data)

    def test_bright_todo(self):
        result = self.client.post("/check-login",
                                data={'email': "brighticorn@email.com", 'password': "password"},
                                follow_redirects=True)
        self.assertIn(b"laundry", result.data)
        self.assertNotIn(b"sweep/mop", result.data)

    def test_pair_todo(self):
        result = self.client.post("/check-login", 
                                data={'email': "pair@programmer.com", 'password': "pass123"},
                                follow_redirects=True)
        self.assertIn(b"sweep/mop", result.data)
        self.assertNotIn(b"laundry", result.data)



def example_data():
    Entry.query.delete()
    Todo.query.delete()
    User.query.delete()
    

    #users
    brighticorn = User(name='Brighticorn', user_id=1, email='brighticorn@email.com', 
        password='password', zipcode='94566')
    pairprogrammer = User(name='PairProgrammer', user_id=2, email='pair@programmer.com',
        password='pass123', zipcode='94588')
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

