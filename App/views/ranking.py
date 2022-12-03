from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for
from flask_jwt import jwt_required
from flask_login import current_user, login_required


from App.controllers import (
    create_ranking, 
    get_all_rankings,
    get_all_rankings_json,
    get_ranking,
    get_rankings_by_image,
    get_rankings_by_creator,
    get_ranking_by_actors,
    get_calculated_ranking,
    update_ranking,
    #delete_ranking,
    get_user,
    get_image
)

ranking_views = Blueprint('ranking_views', __name__, template_folder='../templates')

@ranking_views.route('/rank',methods=['GET'])
def rank_page():
    return render_template('.html')#put template name

@ranking_views.route('/addRanking', methods=['POST'])
@login_required
def add_ranking_action():
    data = request.form
    if data['creatorId']==current_user.id:
        if get_image(data['imageId']):
            prev = get_ranking_by_actors(data['creatorId'], data['imageId'])
            if prev:
                rating=update_ranking(prev.id, data['score'])
                flash('You have given the picture a new ranking!')
                return redirect(url_for(''))
            ranking = create_ranking(data['creatorId'], data['imageId'], data['score'])
            if ranking!=None:
                    flash('You just ranked a picture')
                    return redirect(url_for(''))
        flash('Invalid action, this picture does not exist')#might need to be removed
        return redirect(url_for(''))


@ranking_views.route('/api/rankings', methods=['POST'])
#@login_required
def create_ranking_action():
    data = request.json
    if get_user(data['creatorId']) and get_image(data['imageId']):
        image = get_image(data['imageId'])
        if data['creatorId'] != image.userId:

            prev = get_ranking_by_actors(data['creatorId'], data['imageId'])
            if prev:
                return jsonify({"message":"Current user already ranked this image"}) 
            ranking = create_ranking(data['creatorId'], data['imageId'], data['score'])
            return jsonify({"message":"Ranking created"}) 

        return jsonify({"message":"User cannot rank self"})
    return jsonify({"message":"User not found"}) 

@ranking_views.route('/api/rankings', methods=['GET'])
def get_all_rankings_action():
    rankings = get_all_rankings_json()
    return jsonify(rankings)

@ranking_views.route('/api/rankings/byid', methods=['GET'])
def get_ranking_action():
    data = request.json
    ranking = get_ranking(data['id'])
    if ranking:
        return ranking.toJSON()
    return jsonify({"message":"Ranking Not Found"})

@ranking_views.route('/api/rankings/bycreator', methods=['GET'])
def get_rankings_by_creator_action():
    data = request.json
    if get_user(data['creatorId']):
        ranking = get_rankings_by_creator(data['creatorId'])
        if ranking:
            return jsonify(ranking)
    return jsonify({"message":"User Not Found"})

@ranking_views.route('/api/rankings/byimage', methods=['GET'])
def get_rankings_by_image_action():
    data = request.json
    if get_image(data['imageId']):
        ranking = get_rankings_by_image(data['imageId'])
        if ranking:
            return jsonify(ranking)
    return jsonify({"message":"Image Not Found"})

@ranking_views.route('/api/rankings', methods=['PUT'])
def update_ranking_action():
    data = request.json
    ranking = update_ranking(data['id'], data['score'])
    if ranking:
        return jsonify({"message":"Ranking updated"})
    return jsonify({"message":"Ranking not found"})

# @ranking_views.route('/api/rankings', methods=['DELETE'])
# def delete_ranking_action():
#     data = request.json
#     if get_ranking(data['id']):
#         delete_ranking(data['id'])
#         return jsonify({"message":"Ranking deleted"}) 
#     return jsonify({"message":"Ranking not found"}) 

@ranking_views.route('/api/rankings/calc', methods=['GET'])
def get_calculated_ranking_action():
    data = request.json
    if get_image(data['imageId']):
        ranking = get_calculated_ranking(data['imageId'])
        if ranking:
            return jsonify({"calculated_ranking": ranking}) 
        return jsonify({"message":"No rankings by this image found"})
    return jsonify({"message":"Image not found"})
