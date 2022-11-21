from flask_jwt import jwt_required, current_identity
from flask import Blueprint, render_template, jsonify, request, send_from_directory

from App.controllers import (
    generateProfileList,
    create_user_distributer,
    get_profile_list
)

distributer_views = Blueprint('distributer_views', __name__, template_folder='../templates')

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


@distributer_views.route('/viewprofiles',methods=['GET'])
@jwt_required()
def view_profiles():
    profiles = get_profile_list(current_identity.id)

    return jsonify(profiles)
