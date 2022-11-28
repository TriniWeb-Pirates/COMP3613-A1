from App.models import User
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        user = user.toJSON()
    return user

def get_user(id):
    user=User.query.get(id)
    if user==None:
        return None
    return user

def get_all_users():
    all_Users=User.query.all()
    if all_Users==None:
        return None
    return all_Users

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        db.session.commit()
        return user
    return None

def delete_user(id):
    user = get_user(id)
    if user:
        db.session.delete(user)
        return db.session.commit()
    return None