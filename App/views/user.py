from flask import Flask
from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for
from flask_login import login_required, current_user, LoginManager
from flask_jwt import jwt_required, current_identity




from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user,
    get_user_by_username,
    update_user,
    delete_user,
    login_user,
    logout_user,
    get_level,
    authenticate,
    identity
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/signup',methods=['GET'])
def getSignUpPage():
    return render_template('signup.html')

@user_views.route('/signup',methods=['POST'])
def signupAction():
    data = request.form
    user = get_user_by_username(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"})
    user = create_user(data['username'], data['password'])
    return getLoginPage()


@user_views.route('/login',methods=['GET'])
def getLoginPage():
    return render_template('login.html')

@user_views.route('/login',methods=['POST'])
def loginAction():
    data=request.form
    permittedUser=authenticate(data['username'], data['password'])
    login_user(permittedUser,remember=True)
   # return render_template('home.html', permittedUser=permittedUser) # or can test it with the new home.html page to see how it looks
    return get_user_page()

@user_views.route('/home',methods=['GET'])
@login_required
def get_homePage():
    render_template('home.html',permittedUser=current_user)

@user_views.route('/users', methods=['GET'])
@login_required
def get_user_page():
    users = get_all_users()
    if users==None:
        return redirect(url_for(''))
    return render_template('users.html', users=users)



@user_views.route('/api/users', methods=['GET'])
@login_required
def get_all_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users/byid', methods=['GET'])
@login_required
def get_user_action():
    data = request.form
    user = get_user(data['id'])
    if user:
        return user.toJSON() 
    return jsonify({"message":"User Not Found"})

@user_views.route('/api/users', methods=['PUT'])
@login_required
def update_user_action():
    data = request.form
    user = update_user(data['id'], data['username'])
    if user:
        return jsonify({"message":"User Updated"})
    return jsonify({"message":"User Not Found"})

@user_views.route('/api/users', methods=['DELETE'])
@login_required
def delete_user_action():
    data = request.form
    if get_user(data['id']):
        delete_user(data['id'])
        return jsonify({"message":"User Deleted"}) 
    return jsonify({"message":"User Not Found"}) 

@user_views.route('/api/users/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_identity.username}, id : {current_identity.id}"})

@user_views.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("index.html")