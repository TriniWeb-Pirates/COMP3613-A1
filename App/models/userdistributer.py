from App.database import db
import datetime

class UserDistributer(db.Model):
    DistributerID=db.Column(db.Integer,primary_key=True)
    profiles=db.Column(db.String, nullable=False)# String containing list of profiles for distributing
    userID=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lastRequest= db.Column(db.Date, nullable=False)

    def __init__(self, userID):
        self.userID = userID
        self.profiles = " "
        self.lastRequest = None
    
    def toJSON(self):
        return{
            'DistributerID': self.DistributerID,
            'profiles': self.profiles,
            'userID': self.userID,
            'lastRequest': self.lastRequest
        }

    def generateProfileList():
        
        if datetime.datetime.now() - self.lastRequest < 4: # abitrary:
            return self.profiles
        


        