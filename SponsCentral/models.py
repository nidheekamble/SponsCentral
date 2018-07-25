from SponsCentral import db, login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password= db.Column(db.String(150), nullable=False)
    type= db.Column(db.String(1), nullable=False)
    partyUser= db.relationship("PartyUser", uselist=False, back_populates="user")
    sponsorUser=db.relationship("SponsorUser", uselist=False, back_populates="user")
    conversing = db.relationship("Conversing", back_populates ="user")
    rating = db.Column(db.Float(precision=3, scale=2))

    def __repr__(self):
        return f"User('{self.email}','{self.type}')"

class PartyUser(db.Model):
    __tablename__ = 'partyUser'
    id = db.Column(db.Integer, primary_key=True )
    party_name = db.Column(db.String(30), unique=True , nullable= False)
    party_type = db.Column(db.String(20), unique= False , nullable= False)
    party_kind = db.Column(db.String(20), unique= False , nullable= False)
    party_contactNo1 = db.Column(db.Integer, unique = True , nullable= False )
    party_contactNo2= db.Column(db.Integer, unique = True , nullable= True )
    party_address = db.Column(db.String(300), unique = False , nullable= False)
    party_about = db.Column(db.String(1500), unique= False , nullable= False)
    party_fromAmount = db.Column(db.Integer, unique = False , nullable= False )
    party_toAmount = db.Column(db.Integer, unique = False , nullable= False )
    party_logo = db.Column(db.String(20), unique = False, default = 'default.jpg' , nullable= True )# check on the nullable field
    party_latitude = db.Column(db.Float(precision = 12  ,scale=7) , nullable= True)
    party_longitude = db.Column(db.Float(precision = 12 , scale =7) , nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user = db.relationship("User", back_populates= "partyUser" )
    def __repr__(self):
        return f"PartyUser('{self.party_name}','{self.party_type}','{self.party_kind}','{self.party_contactNo1}','{self.party_contactNo2}','{self.party_address}','{self.party_about}','{self.party_fromAmount}','{self.party_toAmount},'{self.party_logo}')"


class SponsorUser(db.Model):
    __tablename__ = 'sponsorUser'
    id = db.Column(db.Integer, primary_key=True)
    sponsor_name =  db.Column(db.String(30), unique=True , nullable= False)
    sponsor_type = db.Column(db.String(20), unique= False , nullable= False)
    sponsor_kind = db.Column(db.String(20), unique= False , nullable= False)
    sponsor_contactNo1 = db.Column(db.Integer, unique = True , nullable= False )
    sponsor_contactNo2= db.Column(db.Integer, unique = True , nullable= True )
    sponsor_address = db.Column(db.String(300), unique=False , nullable= False)
    sponsor_about = db.Column(db.String(1500), unique=False , nullable= False)
    sponsor_fromAmount =db.Column(db.Integer, unique = False , nullable= False )
    sponsor_toAmount = db.Column(db.Integer, unique = False , nullable= False )
    sponsor_logo = db.Column(db.String(20), unique= False, default = 'default.jpg' , nullable= True )
    sponsor_latitude = db.Column(db.Float(precision=12,scale=7) , nullable= True)
    sponsor_longitude = db.Column(db.Float(precision= 12,scale =7) , nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user = db.relationship("User", back_populates= "sponsorUser" )
    def __repr__(self):
        return f"SponsorUser('{self.sponsor_name}','{self.sponsor_type}','{self.sponsor_kind}','{self.sponsor_contactNo1}','{self.sponsor_contactNo2}','{self.sponsor_address}','{self.sponsor_about}','{self.sponsor_fromAmount}','{self.sponsor_toAmount}','{self.sponsor_logo}')"


class Conversing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= True)
    user = db.relationship("User", back_populates ="conversing")
    user2 = db.Column(db.Integer)
    conversation=db.relationship("Conversation", uselist=False, back_populates ="conversing")
    request = db.Column(db.Integer)
    status = db.Column(db.String(30), nullable=False, default= 'none')
    def __repr__(self):
        return f"Conversing('{self.user1}','{self.user2}','{self.request}','{self.status}')"

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    conversing_id = db.Column(db.Integer, db.ForeignKey('conversing.id'))
    conversing= db.relationship("Conversing", uselist=False, back_populates ="conversation" )
    sender_id = db.Column(db.Integer, unique = False , nullable= False )
    def __repr__(self):
        return f"Conversation('{self.text}','{self.time}','{self.conversing_id}', '{self.sender_id}')"
