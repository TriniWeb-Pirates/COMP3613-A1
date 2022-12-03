from flask_jwt import jwt_required, current_identity
from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_login import login_required, current_user

from App.controllers import (
    generateProfileList,
    create_user_distributer,
    getAllFeeds,
    get_top_profiles,
    getFeed
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


@distributer_views.route('/gettopfeeds',methods=['GET'])
def get_top_rated_view():
    result = get_top_profiles()

    return jsonify(result)

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
    value=1
    return render_template('home.html', profiles=profiles, value=value)


@distributer_views.route('/getallfeeds',methods=['GET'])
def get_all_feeds_view():
    result = getAllFeeds()

    return jsonify(result)