from SponsCentral import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), unique=True)
    password= db.Column(db.Unicode)
    type = db.Column(db.String(1) )
    def __repr__(self):
        return f"User('{self.email}','{self.type}')"

class PartyUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(30), unique=True)
    #party_email= db.Column(db.String(120),unique=True,nullable=False)
    #party_password= db.Column(db.String(150),nullable=False)
    party_type = db.Column(db.String(20), unique= False)
    party_kind = db.Column(db.String(20), unique= False)
    party_contactNo1 = db.Column(db.Integer, unique = True )
    party_contactNo2= db.Column(db.Integer, unique = True )
    party_address = db.Column(db.String(300), unique=True)
    party_about = db.Column(db.String(1500), unique=True)
    party_fromAmount = db.Column(db.Integer, unique = False )
    party_toAmount = db.Column(db.Integer, unique = False )
    party_logo = db.Column(db.String(20), unique= False, default = 'default.jpeg' )# check on the nullable field
    party_latitude = db.Column(db.Float(precision=12,scale=7))
    party_longitude = db.Column(db.Float(precision= 12,scale =7))
    def __repr__(self):
        return f"PartyUser('{self.party_name}','{self.party_type}','{self.party_kind}','{self.party_contactNo1}','{self.party_contactNo2}','{self.party_address}','{self.party_about}','{self.party_fromAmount}','{self.party_toAmount},{self.party_logo}')"


class SponsorUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_name = db.Column(db.String(30), unique=True,)
    #sponsor_email= db.Column(db.String(120),unique=True,nullable=False)
    #sponsor_password= db.Column(db.String(100),nullable=Fals
    sponsor_type = db.Column(db.String(20), unique= False)
    sponsor_kind = db.Column(db.String(20), unique= False)
    sponsor_contactNo1 = db.Column(db.Integer, unique = True )
    sponsor_contactNo2= db.Column(db.Integer, unique = True )
    sponsor_address = db.Column(db.String(300), unique=True)
    sponsor_about = db.Column(db.String(1500), unique=True)
    sponsor_fromAmount = db.Column(db.Integer, unique = False )
    sponsor_toAmount = db.Column(db.Integer, unique = False )
    sponsor_logo = db.Column(db.String(20), unique= False, default = 'default.jpeg' )# check on the nullable field
    sponsor_latitude = db.Column(db.Float(precision=12,scale=7))
    sponsor_longitude = db.Column(db.Float(precision= 12,scale =7))
    def __repr__(self):
        return f"SponsorUser('{self.sponsor_name}','{self.sponsor_type}','{self.sponsor_kind}','{self.sponsor_contactNo1}','{self.sponsor_contactNo2}','{self.sponsor_address}','{self.sponsor_about}','{self.sponsor_fromAmount}','{self.sponsor_toAmount}','{self.sponsor_logo}')"
