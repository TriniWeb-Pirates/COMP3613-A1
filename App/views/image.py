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
    get_images_by_userid,
    get_sorted_images
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')

@image_views.route('/addImage',methods=['GET'])
@login_required
def image_page():
    return render_template('addImage.html')

#route for adding images to a user
@image_views.route('/addImage', methods=['POST'])
@login_required
def add_image():
    data = request.form
    picture=get_image_by_url(current_user.id,data['url'])
    if picture==None:
        image = create_image(current_user.id, data['url'])
        flash("You just added a new picture to your profile!")
        return redirect(url_for('image_views.image_page'))
    flash('You already uploaded this picture')
    return redirect(url_for('image_views.image_page'))


#route for listing all images
@image_views.route('/imageListing', methods=['GET'])
def getImageList():
    images = get_all_images()
    return render_template('image_listing.html', images=images)


#route for providing a list of a user images
@image_views.route('/viewUserImages', methods=['GET'])
@login_required
def viewMyImages():
    rankings, images = get_sorted_images(current_user.id)

    # images = get_images_by_userid(current_user.id)
    images = [image.toJSON() for image in images]

    return render_template('image_listing.html', images=images, rankings=rankings, count = len(images))

#route for removing an image
@image_views.route('/deleteImage/<imageID>', methods=['POST'])
@login_required
def remove_image(imageID):
    if get_image(imageID):
        image=delete_image(imageID)
        if image==None:
            return redirect(url_for('image_views.viewMyImages'))
        return redirect(url_for('image_views.viewMyImages')) 
    return redirect(url_for('image_views.viewMyImages'))

@image_views.route('/getImages', methods=['GET'])
@login_required
def getImages():
    images = get_all_images()
    return render_template('images.html', images=images)


@image_views.route('/getAllImages', methods=['GET'])
@login_required
def get_image_page():
    images = get_all_images()
    return render_template('images.html', images=images)

#Old Routes for postman testing
@image_views.route('/createImage/<userID>', methods=['POST'])
def create_image_action(userID):
    data = request.json
    user = get_user(userID)
    if user:
        image = create_image(userID, data['url'])
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/api/images', methods=['GET'])
def get_images_all_action():
    images = get_all_images_json()
    return jsonify(images)

@image_views.route('/api/createimage', methods=['POST'])
def create_image_api():
    data = request.json
    print(data)
    user = get_user(data['userID'])
    if user:
        image = create_image(data['userID'], "https://i.pinimg.com/originals/87/ce/b3/87ceb3d113d6bc156436be6b9e594c56.jpg")
        return jsonify({"message":"Image created"}) 
    return jsonify({"message":"User does not exist"}) 

@image_views.route('/api/getsortedimages', methods=['GET'])
def get_sorted_images_api():

    get_sorted_images(1)
    # data = request.json
    # print(data)
    # user = get_user(data['userID'])
    # if user:
    #     get_sorted_images(userId)
    #     return jsonify({"message":"Image created"}) 
    # return jsonify({"message":"User does not exist"}) 

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