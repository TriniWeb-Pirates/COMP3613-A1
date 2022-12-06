from flask_jwt import jwt_required, current_identity
from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_login import login_required, current_user

from App.controllers import (
    generateProfileList,
    create_user_distributer,
    getAllFeeds,
    get_top_profiles,
    getFeed,
    distrubuteToUser,
    get_user,
    get_sorted_images
)

distributer_views = Blueprint('distributer_views', __name__, template_folder='../templates')

@distributer_views.route('/generate_profile_feeds',methods=['GET'] )
def generate_profile_feeds():
    result = generateProfileList()
    return jsonify(result)

@distributer_views.route('/createdis',methods=['GET'])
@jwt_required()
def create_new_distributer():
    new_dis = create_user_distributer(current_identity.id)
    return jsonify({"message":"Distributer created"})

@distributer_views.route('/gendis',methods=['GET'])
@jwt_required()
def gendis():
    chosen_users = generateProfileList(current_identity.id)
    return jsonify(chosen_users)


@distributer_views.route('/api/gettopprofiles',methods=['GET'])
def get_top_rated_view():
    result = get_top_profiles()

    profile_list = []
    rating_list = []

    for pair in result:
        profile_list.append(pair[1])
        rating_list.append(pair[0])

    best_images = []

    for profile in profile_list:
        rankings, images  = get_sorted_images(profile)
        if images != None:
            best_image = images[:1][0]
            print(f"profile id {profile} best image is {best_image.id}")
        else:
            print(f"user {profile} has no images!")
    
    return jsonify(result)

@distributer_views.route('/get_top_profiles',methods=['GET'])
def get_highest():
    result = get_top_profiles()

    profile_list = []
    rating_list = []

    for pair in result:
        profile_list.append(pair[1])
        rating_list.append(pair[0])

    best_images = []

    for profile in profile_list:
        rankings, images  = get_sorted_images(profile)
        if images != None:
            best_images.append(images[:1][0])
            
        else:
            best_images.append(f"user {profile} has no images!")
    #use three lists above as data in template
    return render_template('highest_rated_profile.html',profile_list=profile_list, rating_list=rating_list, best_image=best_images)
    #return jsonify(profile_list)



@distributer_views.route('/api/viewprofiles',methods=['GET'])
@jwt_required()
def view_profiles():

    result = generateProfileList()

    if result == 0:
        return jsonify((f"Not enough users to distrubute the required number of feeds."))

    profiles = getFeed(current_identity.id)

    return jsonify(profiles)

    #route to be used for home page to generate the profiles

@distributer_views.route('/viewprofiles',methods=['GET'])
@login_required
def view_profiles_again():

    result = generateProfileList()

    if result==0:
        #return jsonify((f"Not enough users to distrubute the required number of feeds."))
        value=0
        return render_template('home.html', profiles=None, value=value)


    profiles = getFeed(current_user.id)

    if profiles == []:
        profiles = distrubuteToUser(current_user.id)

    value=1
    return render_template('home.html', profiles=profiles, value=value)


@distributer_views.route('/getallfeeds',methods=['GET'])
def get_all_feeds_view():
    result = getAllFeeds()

    return jsonify(result)


@distributer_views.route('/api/getuserfeed',methods=['GET'])
@jwt_required()
def get_user_feed_api():
    return jsonify(getFeed(current_identity.id))