from App.database import db
import datetime

class UserDistributer(db.Model):

    __tablename__ = "UserDistributer"

    id = db.Column(db.Integer, primary_key=True)
    # feeds = db.relationship('Profilefeed', backref='profilefeed', lazy=True, cascade="all, delete-orphan")
    num_profiles = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.Date)

    def __init__(self, num_profiles):
        self.num_profiles = num_profiles
        self.timestamp = datetime.datetime.now()
    
    def toJSON(self):
        return{
            'DistributerID': self.id,
            'num_profiles': self.num_profiles,
            'timestamp': self.timestamp
        }

      

        


        