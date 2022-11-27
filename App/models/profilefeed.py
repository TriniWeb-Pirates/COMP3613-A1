from App.database import db
class ProfileFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # senderID =  db.Column(db.Integer, nullable=False)
    # recieverID =  db.Column(db.Integer, nullable=False)

    # senderID = db.relationship('User', backref='User', lazy=True, cascade="all, delete-orphan")
    # recieverID = db.relationship('User', backref='User', lazy=True, cascade="all, delete-orphan")

    senderID =  db.Column(db.Integer,nullable=False)#senderID is the ID of the profile you are sending
    recieverID =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#recieverID is ID of a person who recieves the distributed profiles

    # sender = db.relationship("User", foreign_keys=[senderID])
    # recieverID = db.relationship("User", foreign_keys=[recieverID])

    seen = db.Column(db.Boolean, default=False, nullable=False)
    distributerID = db.Column(db.Integer, db.ForeignKey('userdistributer.id'), nullable=False)
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
            'rating': self.rating
        }
