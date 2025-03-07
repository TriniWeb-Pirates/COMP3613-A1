from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash
from flask_jwt import jwt_required
from flask_login import current_user, login_required


from App.controllers import (
    create_rating, 
    get_all_ratings,
    get_all_ratings_json,
    get_rating,
    get_all_total_ratings,
    get_ratings_by_target,
    get_ratings_by_creator,
    get_rating_by_actors,
    update_rating,
    get_user,
    get_calculated_rating
)

rating_views = Blueprint('rating_views', __name__, template_folder='../templates')

#route for adding a rating to a profile
@rating_views.route('/addRating/<targetId>', methods=['POST'])
@login_required
def add_Rating(targetId):
    value=request.form
    data=int(value['score'])
    if get_user(targetId):
        prev = get_rating_by_actors(current_user.id, targetId)
        if prev:#Rerate profile
            rating=update_rating(prev.id, data)
            flash('You have given the profile a new rating!')
            return redirect('/viewUserProfile/<targetId>')
        rating = create_rating(current_user.id, targetId, data)#Rate profile
        if rating!=None:
            flash('You just rated another profile')
            return redirect('/viewUserProfile/<targetId>')
            
#old routes for postman testing
@rating_views.route('/api/ratings', methods=['POST'])
def create_rating_action():
    data = request.json
    if get_user(data['creatorId']) and get_user(data['targetId']):
        if data['creatorId'] != data['targetId']:
            prev = get_rating_by_actors(data['creatorId'], data['targetId'])
            if prev:
                return jsonify({"message":"Current user already rated this user"}) 
            rating = create_rating(data['creatorId'], data['targetId'], data['score'])
            return jsonify({"message":"Rating created"}) 
        return jsonify({"message":"User cannot rate self"})
    return jsonify({"message":"User not found"}) 

@rating_views.route('/api/ratings', methods=['GET'])
def get_all_ratings_action():
    ratings = get_all_ratings_json()
    return jsonify(ratings)

@rating_views.route('/api/ratings/byid', methods=['GET'])
def get_rating_action():
    data = request.json
    rating = get_rating(data['id'])
    if rating:
        return rating.toJSON()
    return jsonify({"message":"Rating not found"})

@rating_views.route('/api/ratings/bycreator', methods=['GET'])
def get_rating_by_creator_action():
    data = request.json
    if get_user(data['creatorId']):
        rating = get_ratings_by_creator(data['creatorId'])
        if rating:
            return jsonify(rating) 
        return jsonify({"message":"No ratings by this user found"})
    return jsonify({"message":"User not found"})

@rating_views.route('/api/ratings/bytarget', methods=['GET'])
def get_rating_by_target_action():
    data = request.json
    if get_user(data['targetId']):
        rating = get_ratings_by_target(data['targetId'])
        if rating:
            return jsonify(rating) 
        return jsonify({"message":"No ratings for this user found"})
    return jsonify({"message":"User not found"})

@rating_views.route('/api/ratings', methods=['PUT'])
def update_rating_action():
    data = request.json
    rating = update_rating(data['id'], data['score'])
    if rating:
        return jsonify({"message":"Rating updated"})
    return jsonify({"message":"Rating not found"})

# @rating_views.route('/api/ratings', methods=['DELETE'])
# def delete_rating_action():
#     data = request.json
#     if get_rating(data['id']):
#         delete_rating(data['id'])
#         return jsonify({"message":"Rating deleted"}) 
#     return jsonify({"message":"Rating not found"}) 

@rating_views.route('/api/ratings/all', methods=['GET'])
def get_all_total_ratings_view():
    result = get_all_total_ratings()
    return (str(result))

@rating_views.route('/api/ratings/calc', methods=['GET'])
def get_calculated_rating_action():
    data = request.json
    if get_user(data['targetId']):
        rating = get_calculated_rating(data['targetId'])
        if rating:
            return jsonify({"calculated rating": rating}) 
        return jsonify({"message":"No ratings by this user found"})
    return jsonify({"message":"User not found"})

