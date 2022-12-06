from App.models import User, UserDistributer, ProfileFeed
from App.controllers import user, profilefeed
from App.database import db
import random, datetime


viewing_size = 5 #size of each user's feed
update_interval = 8600

def create_user_distributer(num_profiles):
    new_distributer = UserDistributer(num_profiles)
    db.session.add(new_distributer)
    db.session.commit()
    return new_distributer

def checkPopulation(popsize, viewieng_size):

    if popsize < viewieng_size + 1:
        return 0
    
    return 1


def checkRecency():
    distributer_history = UserDistributer.query.all()

    if distributer_history != []:

        last_request = distributer_history[-1].timestamp
        
        time_delta = datetime.datetime.now() - last_request
        
        if time_delta.total_seconds() < update_interval:
            return 0
    
    return 1

def update_last_distributer(profiles):
    last_distributer = UserDistributer.query.all()[-1]

    if last_distributer:
        last_distributer.num_profiles += profiles
        db.session.add(last_distributer)
        db.session.commit()
        return last_distributer
    return None


def distrubuteToUser(userID):
    profiles = user.get_all_users_json()

    profiles.pop(int(userID - 1))
    
    feed_profiles = random.sample(profiles, viewing_size)

    last_distributer = update_last_distributer(viewing_size)

    new_feed = []
    for profile in feed_profiles:
        new_feed.append(ProfileFeed(profile["id"], userID, last_distributer.id))

    for feed in new_feed:
            profilefeed.commit_feed(feed)

    return [feed.toJSON() for feed in new_feed]

def generateProfileList():

    profiles = user.get_all_users_json()

    if len(profiles) < viewing_size + 1:
        return 0

    distributer_history = UserDistributer.query.all()

    if distributer_history != []:

        last_request = distributer_history[-1].timestamp
        
        time_delta = datetime.datetime.now() - last_request
        
        if time_delta.total_seconds() < update_interval:
            return 1
    
    new_distribution = create_user_distributer(len(profiles))

    profiles_distributed = 0

    # include check for total users < viewieng_size

    #loop through each user and create feeds for them 

    for profile in profiles:
        #user1
        #[1, 2, 3, 4, 5, 6,]
        current_user_id = profile["id"]

        potential_profiles = profiles.copy()
        potential_profiles.pop(int(current_user_id - 1)) # removes current user from potential users to be in feed
        
        user_feed = profilefeed.getFeed(current_user_id)

        profiles_neeeded = viewing_size

        for feed in user_feed:
            # add old unviewed profiles to new feed
            if feed['seen'] == False:
                profiles_neeeded -= 1
                for i in potential_profiles:
                    if i['id'] == feed['senderID']:
                        potential_profiles.remove(i)
                        break
                # print(potential_profiles)
                # potential_profiles.pop(int( - 1 )) # removes seen profiles from feed


        # get new users to fill feed

        new_profiles = random.sample(potential_profiles, profiles_neeeded)

        # make feed objects for the profiles added to a users feed 

        new_feed = []
        for profile in new_profiles:
            new_feed.append(ProfileFeed(profile["id"], current_user_id, new_distribution.id))

        # commit feed objects to feed table
        for feed in new_feed:
            profilefeed.commit_feed(feed)

    return("complete")
