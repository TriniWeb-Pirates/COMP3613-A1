from App.database import db
import datetime

class UserDistributer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_profiles = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.Date)

    def __init__(self):
        self.timestamp = datetime.datetime.now()
    
    def toJSON(self):
        return{
            'DistributerID': self.id,
            'num_profiles': self.num_profiles,
            'timestamp': self.timestamp
        }

      

        


        