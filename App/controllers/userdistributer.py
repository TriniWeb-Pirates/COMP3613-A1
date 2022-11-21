from App.models import User, UserDistributer
from App.controllers import user
from App.database import db
import random

def create_user_distributer(userid):
    new_distributer = UserDistributer(userid)
    db.session.add(new_distributer)
    db.session.commit()
    return new_distributer
    
def generateProfileList(current_user_id):

    viewing_size = 5

    profile_string = ""
    # get the users userdistrubuter

    current_distrubuter = UserDistributer.query.filter_by(userID=current_user_id).first()

    #check last request

    #if request was recent
    # if datetime.datetime.now() - current_distrubuter.lastRequest < 4:
    #     pass
        # return either the current list of profiles or some error saying requet too recent

    #generate the list of users to view

    users = user.get_all_users_json()

    # users.remove(int(current_user_id) - 1)
    # include check for total users < viewieng_size
    chosen_users = random.sample(users, viewing_size)

    for x in chosen_users:
        profile_string += str(x['id']) + '_'
    
    current_distrubuter.profiles = profile_string
    db.session.add(current_distrubuter)
    db.session.commit()

    return(profile_string)

def get_profile_list(current_user_id):
    profile_list = UserDistributer.query.filter_by(userID=current_user_id).first().profiles

    return profile_list
    

