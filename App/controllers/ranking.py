from App.models import Ranking, User, Image
from App.database import db

def create_ranking(creatorId, imageId, score):
    newRanking = Ranking(creatorId=creatorId, imageId=imageId, score=score)
    db.session.add(newRanking)
    db.session.commit()
    return newRanking

def get_rankings_by_creator(creatorId):
    ranking=Ranking.query.filter_by(creatorId=creatorId)
    if ranking==None:
        return None
    return ranking

def get_rankings_by_image(imageId):
    ranking=Ranking.query.filter_by(imageId=imageId)
    if ranking==None:
        return None
    return ranking

def get_ranking(id):
    ranking = Ranking.query.get(id)
    if ranking==None:
        return None
    return ranking

def get_all_rankings():
    return Ranking.query.all()

def get_all_rankings_json():
    rankings = Ranking.query.all()
    if not rankings:
        return []
    rankings = [ranking.toJSON() for ranking in rankings]
    return rankings

def get_rankings_by_creator(creatorId):
    rankings = Ranking.query.filter_by(creatorId=creatorId)
    if not rankings:
        return []
    rankings = [ranking.toJSON() for ranking in rankings]
    return rankings

def get_rankings_by_image(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId)
    if not rankings:
        return []
    rankings = [ranking.toJSON() for ranking in rankings]
    return rankings

def get_ranking_by_actors(creatorId, imageId):
    if User.query.get(creatorId) and Image.query.get(imageId):
        ranking = Ranking.query.filter_by(creatorId=creatorId, imageId=imageId).first()
        return ranking
    return None

def get_ranking_by_user(creatorId,score):
    if Ranking.query.get(creatorId):
        ranking = Ranking.query.filter_by(creatorId=creatorId, score=score).first()
        return ranking
    return None

def update_ranking(id, score):
    ranking = get_ranking(id)
    if ranking:
        ranking.score = score
        db.session.add(ranking)
        db.session.commit()
        return ranking
    return None

def delete_ranking(id):
    ranking = get_ranking(id)
    if ranking:
        db.session.delete(ranking)
        return db.session.commit()
    return None
    
def get_calculated_ranking(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId)
    total = 0
    if rankings:
        for ranking in rankings:
            total = total + ranking.score
        if rankings.count() != 0:
            total = total / rankings.count()
        return total
    return None