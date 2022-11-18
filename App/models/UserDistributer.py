from App.database import db
from datetime import date

class UserDistributer(db.Model):
    DistributerID=db.Column(db.Integer,primary_key=True)
    #profiles=db.Column()# Column 
    userID=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lastRequest= db.Column(db.Date, nullable=False)

    def __init__(self,userID,lastRequest):

        self.userID = userID
        self.lastRequest = lastRequest
    
    def toJSON(self):
        return{
            'DistributerID': self.DistributerID,
            'userID': self.userID,
            'lastRequest': self.lastRequest
        }