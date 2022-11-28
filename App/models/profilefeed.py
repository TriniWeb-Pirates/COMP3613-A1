from App.database import db

class ProfileFeed(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    senderID =  db.Column(db.Integer,nullable=False)#senderID is the ID of the profile you are sending
    recieverID =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#recieverID is ID of a person who recieves the distributed profiles
    seen = db.Column(db.Boolean, default=False, nullable=False)
    distributerID = db.Column(db.Integer, db.ForeignKey('userdistributer.id'), nullable=True)
    rating =  db.Column(db.Integer, db.ForeignKey('rating.id'), default = None, nullable=True)
    
    def __init__(self, senderID, recieverID, distributerID):
        self.senderID = senderID
        self.recieverID = recieverID
        self.distributerID = distributerID

    def toJSON(self):
        return{
            'id': self.id,
            'senderID': self.senderID,
            'recieverID': self.recieverID,
            'distributerID': self.distributerID,
            'seen': self.seen,
            'rating': self.rating
        }
