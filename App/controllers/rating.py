from App.models import Rating, User
from App.controllers import user
from App.database import db

def create_rating(creatorId, targetId, score):
    if score == 0:
        return None
    newRating = Rating(creatorId=creatorId, targetId=targetId, score=score)
    db.session.add(newRating)
    db.session.commit()
    return newRating

def get_ratings_by_target(targetId):
    ratings = Rating.query.filter_by(targetId=targetId)
    if not ratings:
        return []
    ratings = [rating.toJSON() for rating in ratings]
    return ratings

def get_ratings_by_creator(creatorId):
    ratings = Rating.query.filter_by(creatorId=creatorId)
    if not ratings:
        return []
    ratings = [rating.toJSON() for rating in ratings]
    return ratings

def get_rating_by_actors(creatorId, targetId):
    if User.query.get(creatorId) and User.query.get(targetId):
        rating = Rating.query.filter_by(creatorId=creatorId, targetId=targetId).first()
        return rating
    return None

def get_rating(id):
    rating = Rating.query.get(id)
    if rating==None:
        return None
    return rating

def get_all_ratings():
    return Rating.query.all()

def get_all_ratings_json():
    ratings = Rating.query.all()
    if not ratings:
        return []
    ratings = [rating.toJSON() for rating in ratings]
    return ratings

def update_rating(id, score):
    rating = get_rating(id)
    if rating:
        rating.score = score
        db.session.add(rating)
        db.session.commit()
        return rating
    return None

# def delete_rating(id):
#     rating = get_rating(id)
#     if rating:
#         db.session.delete(rating)
#         return db.session.commit()
#     return None

def get_calculated_rating(targetId):
    ratings = Rating.query.filter_by(targetId=targetId).all()
    total = 0

    x=0

    if ratings:
        for rating in ratings:
            total = total + rating.score
            x = x + 1
        
        if(x!=0):
            avg = total/x
            print(avg)
            return avg

        return None
        

  
        

def get_all_total_ratings():
    profiles = user.get_all_users_json()

    profile_ratings = []

    for profile in profiles:
        profile_ratings.append(get_calculated_rating(profile["id"]))

    return profile_ratings

def get_top_profiles():
    
    viewing_size = 3

    profile_ratings = get_all_total_ratings()

    top_profiles = {}

    for i in range(viewing_size):

        highest_val = max(profile_ratings)
        highest_index = profile_ratings.index(highest_val)
        profile_ratings.pop(highest_index)

        profile_value = "User " + str(highest_index + 1)

        top_profiles[profile_value] = highest_val

    return top_profiles

def get_level(id):
    ratings = get_ratings_by_creator(id)
    if ratings:
        level = 0
        for rating in ratings:
            level = level + 1
        return level
    return None