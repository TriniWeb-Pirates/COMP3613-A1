from App.models import Image
from App.controllers import ranking
from App.database import db

def create_image(userId, url):
    newImage = Image(userId=userId, url=url)
    db.session.add(newImage)
    db.session.commit()
    return newImage

def get_image(id):
    return Image.query.get(id)

def get_image_by_url(userId,url):
    picture=Image.query.filter_by(userId=userId,url=url).first()
    if picture==None:
        return None
    return picture

def get_image_json(id):
    image = Image.query.get(id)
    if not image:
        return []
    image = image.toJSON()
    return image

def get_images_by_userid(userId):
    return Image.query.filter_by(userId=userId).all()
    
def get_user_image_count(userId):
    images=Image.query.filter_by(userId=userId).all()
    count=0
    for image in images:
        count=count+1
    return count

def get_images_by_userid_json(userId):
    images = Image.query.filter_by(userId=userId)
    if not images:
        return []
    images = [image.toJSON() for image in images]
    return images

def get_sorted_images(userId):
    images = Image.query.filter_by(userId=userId)
    if not images:
        return []

    rankings = []

    for image in images:
        rankings.append(ranking.get_calculated_ranking(image.id))

    print(rankings)
    
    paired_lists = zip(rankings, images)

    sorted_lists = sorted(paired_lists, reverse=True,  key = lambda x: x[0])

    unpaired_tuples = zip(*sorted_lists)

    rankings, images = [pair for pair in unpaired_tuples]
    
    return rankings, images
    
def get_all_images():
    return Image.query.all()

def get_all_images_json():
    images = Image.query.all()
    if images:
        images = [image.toJSON() for image in images]
        return images
    return []

def delete_image(id):
    image = get_image(id)
    if image:
        db.session.delete(image)
        return db.session.commit()
    return None