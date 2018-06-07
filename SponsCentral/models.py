from SponsCentral import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password= db.Column(db.String(150), nullable=False)
    type= db.Column(db.String(1), nullable=False)
    def __repr__(self):
        return f"User('{self.email}','{self.type}')"

class PartyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    party_name = db.Column(db.String(30), unique=True , nullable= False)
    party_type = db.Column(db.String(20), unique= False , nullable= False)
    party_kind = db.Column(db.String(20), unique= False , nullable= False)
    party_contactNo1 = db.Column(db.Integer, unique = True , nullable= False )
    party_contactNo2= db.Column(db.Integer, unique = True , nullable= True )
    party_address = db.Column(db.String(300), unique = True , nullable= False)
    party_about = db.Column(db.String(1500), unique= False , nullable= False)
    party_fromAmount = db.Column(db.Integer, unique = False , nullable= False )
    party_toAmount = db.Column(db.Integer, unique = False , nullable= False )
    party_logo = db.Column(db.String(20), unique = False, default = 'default.jpeg' , nullable= True )# check on the nullable field
    party_latitude = db.Column(db.Float(precision = 12  ,scale=7) , nullable= True)
    party_longitude = db.Column(db.Float(precision = 12 , scale =7) , nullable= True)
    def __repr__(self):
        return f"PartyUser('{self.party_name}','{self.party_type}','{self.party_kind}','{self.party_contactNo1}','{self.party_contactNo2}','{self.party_address}','{self.party_about}','{self.party_fromAmount}','{self.party_toAmount},{self.party_logo}')"


class SponsorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_name =  db.Column(db.String(30), unique=True , nullable= False)
    sponsor_type = db.Column(db.String(20), unique= False , nullable= False)
    sponsor_kind = db.Column(db.String(20), unique= False , nullable= False)
    sponsor_contactNo1 = db.Column(db.Integer, unique = True , nullable= False )
    sponsor_contactNo2= db.Column(db.Integer, unique = True , nullable= True )
    sponsor_address = db.Column(db.String(300), unique=True , nullable= False)
    sponsor_about = db.Column(db.String(1500), unique=True , nullable= False)
    sponsor_fromAmount =db.Column(db.Integer, unique = False , nullable= False )
    sponsor_toAmount = db.Column(db.Integer, unique = False , nullable= False )
    sponsor_logo = db.Column(db.String(20), unique= False, default = 'default.jpeg' , nullable= True )
    sponsor_latitude = db.Column(db.Float(precision=12,scale=7) , nullable= True)
    sponsor_longitude = db.Column(db.Float(precision= 12,scale =7) , nullable= True)
    def __repr__(self):
        return f"SponsorUser('{self.sponsor_name}','{self.sponsor_type}','{self.sponsor_kind}','{self.sponsor_contactNo1}','{self.sponsor_contactNo2}','{self.sponsor_address}','{self.sponsor_about}','{self.sponsor_fromAmount}','{self.sponsor_toAmount}','{self.sponsor_logo}')"

class Region(db.Model):
    region_id=db.Column(db.Integer,primary_key=True)
    region_name=db.Column(db.String(50),nullable=False)
    state=db.Column(db.String(40),nullable=False)
    city=db.Column(db.String(40),nullable=False)
    latitude = db.Column(db.Float(precision = 12  ,scale=7) , nullable= False)
    longitude = db.Column(db.Float(precision = 12 , scale =7) , nullable= False)
