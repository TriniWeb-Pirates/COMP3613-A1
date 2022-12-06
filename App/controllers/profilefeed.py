from App.models import ProfileFeed, UserDistributer
from App.controllers import userdistributer
from App.database import db

def create_profile_feed(senderID, recieverID, distributerID):
    new_feed = ProfileFeed(senderID, recieverID, distributerID)
    db.session.add(new_feed)
    db.session.commit()
    return new_feed

def commit_feed(profile_feed):
    db.session.add(profile_feed)
    db.session.commit()
    return profile_feed

def getFeed(userID):

    last_distributer = UserDistributer.query.all()[-1]

    user_feed =  ProfileFeed.query.filter_by(recieverID=userID, distributerID = last_distributer.id)

    user_feed = [feed.toJSON() for feed in user_feed]


    return user_feed

def view_feed(userID, targetID):
    
    user_feed = ProfileFeed.query.filter_by(recieverID=userID, senderID=targetID, seen = False).first()

    if user_feed is None:
        return None

    user_feed.seen = True
    
    db.session.add(user_feed)
    db.session.commit()

    return 1

def getAllFeeds():
    
    feeds = ProfileFeed.query.all()

    if not feeds:
        return []
    feeds = [feed.toJSON() for feed in feeds]

    return feeds