from App.models import ProfileFeed
from App.database import db

def create_profile_feed(senderID, recieverID, distributerID):
    new_feed = ProfileFeed(senderID, recieverID, distributerID)
    db.session.add(new_feed)
    db.session.commit()
    return new_feed

def commit_feed(profile_feed):
    db.session.add(new_feed)
    db.session.commit()
    return new_feed

def getFeed(userID):

    return ProfileFeed.query.filter_by(recieverID=userID)

def getAllFeeds():
    
    feeds = ProfileFeed.query.all()
    if not feeds:
        return []
    feeds = [feed.toJSON() for feed in feeds]
    return feeds