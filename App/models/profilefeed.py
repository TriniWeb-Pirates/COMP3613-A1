from App.database import db
from App.controllers import rating

class ProfileFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderID =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recieverID =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    distributerID = db.Column(db.Integer, db.ForeignKey('userdistributer.id'), nullable=False)
    seen = db.Column(db.Boolean, default=False, nullable=False)
    rating =  db.Column(db.Integer, db.ForeignKey('rating.id'), default = None, nullable=True)
    
    
    def __init__(self, senderID, recieverID, distributerID):
        self.senderID = senderID
        self.recieverID = recieverID
        self.distributerID = distributerID

    
    def toJSON(self):
        return{
            'id': self.id,
            'senderID': self.creatorId,
            'recieverID': self.imageId,
            'distributerID': self.score,
            'rating' : rating.get_rating(self.rating)
        }
