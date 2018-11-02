"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """create users in database"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(25), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)    

    def __repr__(self):
            """Provide helpful representation when printed."""
            return f"<User user_id={self.user_id} email={self.email}>"


class Entry(db.Model):
    """create entries in database"""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(10000), nullable=False)
    quote = db.Column(db.String(1000), nullable=False)
    weather = db.Column(db.String(50), nullable=False)

    #relationship#
    user = db.relationship("User", backref = db.backref("entries"))

    def __repr__(self):
            """Provide helpful representation when printed."""
            return f"<Entry date={self.date} user={self.user_id}>"


class Todo(db.Model):
    """create todos in database"""

    __tablename__ = "todos"

    todo_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    todo = db.Column(db.String(1000))
    
    #relationship#
    user = db.relationship("User", backref = db.backref("todos"))

    def __repr__(self):
            """Provide helpful representation when printed."""
            return f"<Todo user={self.user_id} todo_id={self.todo_id}>"
  

############################################################################
def connect_to_db(app, db_uri='postgresql:///journals'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to DB.")