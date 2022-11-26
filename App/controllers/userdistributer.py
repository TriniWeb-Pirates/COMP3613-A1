from App.models import User, UserDistributer, ProfileFeed
from App.controllers import user, profilefeed
from App.database import db
import random

def create_user_distributer(num_profiles):
    new_distributer = UserDistributer(num_profiles)
    db.session.add(new_distributer)
    db.session.commit()
    return new_distributer
    
def generateProfileList(current_user_id):

    viewing_size = 5

    # check if new feed are allowed to generated
    last_request = UserDistributer.query.all().first()
    
    if datetime.datetime.now() - last_request < 8600:
        return None

    users = user.get_all_users_json()

    new_distribution = create_user_distributer(len(users))

    profiles_distributed = 0

    # users.remove(int(current_user_id) - 1)
    # include check for total users < viewieng_size

    #loop through each user and create feeds for them 

    for user in users:
        all_users = users.copy()

        potential_profiles = all_users.pop(int(current_user_id + 1)) # removes current user from potential users to be in feed

        user_feed = profilefeed.getFeed(user['ID'])
        new_feed = []

        for feed in user_feed:
            # add old unviewed profiles to new feed
            if feed['seen'] == False:
                new_feed.append(feed)
                potential_profiles.pop(int(feed['senderID'] + 1 )) # removes seen profiles from feed

        # add users to need to fill feed

        profiles_neeeded = len(feed) != viewing_size

        new_profiles = random.sample(potential_profiles, profiles_neeeded)

        # make feed objects for the profiles added to a users feed 

        for profile in new_profiles:
            new_feed = ProfileFeed(profile["ID"], current_user_id, new_distribution.id)

        # commit feed objects to feed table; new and old profiles are added simultaenously this way 
        for feed in new_feed:
            profilefeed.commit_feed(feed)

    return("complete")

def get_profile_list(current_user_id):
    profile_list = UserDistributer.query.filter_by(userID=current_user_id).first().profiles

    return profile_list
    

