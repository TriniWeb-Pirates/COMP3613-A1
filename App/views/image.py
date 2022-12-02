from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect, url_for, flash
from flask_jwt import jwt_required
from flask_login import login_required, current_user


from App.controllers import (
    create_image, 
    get_all_images,
    get_all_images_json,
    get_images_by_userid_json,
    get_image,
    get_image_json,
    delete_image,
    get_user,
    get_image_by_url,
    get_images_by_userid
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')

@image_views.route('/addImage',methods=['GET'])
@login_required
def image_page():
    return render_template('addImage.html')

@image_views.route('/addImage', methods=['POST'])
@login_required
def add_image():
    data = request.form
    picture=get_image_by_url(data['url'])
    if picture==None:
        image = create_image(current_user.id, data['url'])
        flash("You just added a new picture to your profile!")
        return redirect(url_for('image_views.image_page'))
    flash('You already uploaded this picture')
    return redirect(url_for('image_views.image_page'))

@image_views.route('/imageListing', methods=['GET'])
def getImageList():
    images = get_all_images()
    return render_template('image_listing.html', images=images)

@image_views.route('/viewUserImages', methods=['GET'])
@login_required
def viewMyImages():
    images=get_images_by_userid(current_user.id)
    if images:
        flash('You must add images to your profile to view them')
        return redirect(url_for('image_views.image_page'))
    return render_template('image_listing.html',user_images=images)


@image_views.route('/deleteImage/<imageID>', methods=['DELETE'])
@login_required
def remove_image(imageID):
    if get_image(imageID):
        image=delete_image(imageID)
        if image==None:
            return redirect(url_for('image_views.viewMyImages'))
        return redirect(url_for('image_views.viewMyImages')) 
    return redirect(url_for('image_views.viewMyImages'))

#Old Routes for testing
@image_views.route('/getImages', methods=['GET'])
def getImages():
    images = get_all_images()
    return render_template('images.html', images=images)


@image_views.route('/getAllImages', methods=['GET'])
@login_required
def get_image_page():
    images = get_all_images()
    return render_template('images.html', images=images)

@image_views.route('/createImage/<userID>', methods=['POST'])
#@login_required
def create_image_action(userID):
    data = request.form
    user = get_user(userID)
    if user:
        image = create_image(userID, data['url'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/api/images', methods=['GET'])
def get_images_all_action():
    images = get_all_images_json()
    return jsonify(images)

@image_views.route('/api/images/<userID>', methods=['GET'])
@login_required
def get_images_by_user_action(userID):
    images = get_images_by_userid_json(userID)
    return jsonify(images)

@image_views.route('/api/images/<imageID>', methods=['GET'])
@login_required
def get_images_by_id_action(imageID):
    image = get_image_json(imageID)
    return jsonify(image)

@image_views.route('/api/images/<imageID>', methods=['DELETE'])
@login_required
def delete_image_action(imageID):
    if get_image(imageID):
        delete_image(imageID)
        return jsonify({"message":"Image Deleted"}) 
    return jsonify({"message":"Image Not Found"}) 