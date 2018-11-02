"""seed info to make database"""

from sqlalchemy import func
from model import User, Entry, Todo, connect_to_db, db
from server import app
from datetime import datetime 
import hashlib

def load_users():
    """Load users from users.item into database."""

    print("Users")
    User.query.delete()

    for row in open("seed_data/user.item"):
        row = row.rstrip()
        user_id, name, email, password, zipcode = row.split("|")
        # hash password
        password = password.encode()
        hash_password = hashlib.sha256(password)
        hash_password = hash_password.hexdigest()
        
        user = User(user_id = user_id,
                    name = name,
                    email = email,
                    password = hash_password,
                    zipcode = zipcode)
        db.session.add(user)
    db.session.commit()


def load_entries():
    """Load entries from entries.item into database."""

    print("Entires")

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
    """Load todos from todo.item into database."""

    print("Todos")

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
    """Set value for the next todo_id after seeding database"""

    # Get the Max todo_id in the database
    result = db.session.query(func.max(Todo.todo_id)).one()
    max_id = int(result[0])
    # Set the value for the next todo_id to be max_id + 1
    query = "SELECT setval('todos_todo_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_entry_id():
    """Set value for the next entry_id after seeding database"""

    # Get the Max entry_id in the database
    result = db.session.query(func.max(Entry.entry_id)).one()
    max_id = int(result[0])
    # Set the value for the next entry_id to be max_id + 1
    query = "SELECT setval('entries_entry_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()
    load_users()
    load_entries()
    load_todos()
    set_val_user_id()
    set_val_todo_id()
    set_val_entry_id()
