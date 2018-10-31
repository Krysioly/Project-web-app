"""seed info to make database"""

from sqlalchemy import func
from model import User
from model import Entry
from model import Todo

from model import connect_to_db, db
from server import app

from datetime import datetime 


def load_users():
    """Load users from u.user into database."""

    print("Users")

    User.query.delete()

    # Read user file and insert data
    for row in open("seed_data/user.item"):
        row = row.rstrip()
        user_id, name, email, password, zipcode = row.split("|")

        user = User(user_id = user_id,
                    name = name,
                    email = email,
                    password = password,
                    zipcode = zipcode)

        db.session.add(user)

    db.session.commit()


def load_entries():
    """Load users from u.user into database."""

    print("Entires")

    # Read entires file and insert data
    for row in open("seed_data/entries.item"):

        row = row.rstrip()
        date, user_id, title, text, quote, weather = row.split("|")

        entry = Entry(date = date,
                    user_id = user_id,
                    title = title,
                    text = text,
                    quote = quote,
                    weather = weather)

        db.session.add(entry)

    db.session.commit()


def load_todos():
    """Load users from u.user into database."""

    print("Todos")

    # Read entires file and insert data
    for row in open("seed_data/todo.item"):

        row = row.rstrip()
        todo_id, user_id, todo = row.split("|")

        todo = Todo(todo_id = todo_id,
                    user_id = user_id,
                    todo = todo)

        db.session.add(todo)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_todo_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Todo.todo_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('todos_todo_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_entry_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Entry.entry_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('entries_entry_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()



if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_entries()
    load_todos()
    set_val_user_id()
    set_val_todo_id()
    set_val_entry_id()
